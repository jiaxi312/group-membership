import random
import time
import datetime

from message import Message
from threading import Timer


class Processor:
    """A class represents a single Processor in the membership system

    A Processor represents the abstract concept of Processor or Server in Cristian’s
    "Reaching Agreement on Processor Group Membership in Synchronous Distributed Systems" paper.
    A Processor can send a direct message to other processor or broadcast to all correct processors. It also keeps track
    of its status, its view of the membership of group T. It may also contain clock synchronization error when
    initialized.

    Attributes:
        _id: A int indicating the id of this Processor
        _current_group: A str indicating the current group the processor belongs to
        _status: A int constant indicating the status of the Processor
        _membership: A list contains the Processor's view of its memberships in the _current_group
        _channel: A Channel object where the processor is attached to
        _clock_diff: A float representing the clock synchronization error of this Processor clock from the master clock
        _check_timer: A timer object that schedules sending the present message
        _check_in_period: A float indicates the check in period for the processor
    """

    NORMAL = 1
    CRASHED = -1
    ID_COUNT = 1

    PERIODIC_BROADCAST_PROTOCOL = 10
    ATTENDANCE_LIST_PROTOCOL = 11
    NEIGHBOR_SURVEILLANCE_PROTOCOL = 12

    def __init__(self, channel, max_clock_sync_error, check_in_period, check_in_policy):
        """ Inits the Processor with given max clock synchronization error """
        self._id = Processor.ID_COUNT
        self._current_group = 0
        self._status = Processor.NORMAL
        self._membership = set()
        self._channel = channel
        self._max_clock_sync_error = max_clock_sync_error
        self._clock_diff = (random.random() - 0.5) * max_clock_sync_error
        self._check_timer = None
        self._check_member_timer = None
        self._check_in_period = check_in_period
        self._check_in_ids_count = set()
        self._protocol = check_in_policy
        self._attendance_list_checked = False
        Processor.ID_COUNT += 1

    def init_join(self):
        """Initializes the join process, broadcasting the new-group message to all correct processors."""
        print(f'processor {self.id} init group')
        self._membership = set()
        m = self._channel.create_message(self, Message.NEW_GROUP)
        broadcast_delay = self._channel.broadcast_delay
        m.content = self.clock + datetime.timedelta(seconds=broadcast_delay + self._max_clock_sync_error)
        self._channel.broadcast(m)

    def send(self, target):
        """Sends the given message to target processor"""
        m = self._channel.create_message(self)
        m.receiver = target
        self._channel.send_message(m)

    def broadcast_present_msg(self, V):
        """Broadcasts the present message to all correct processors"""
        m = self._channel.create_message(self, Message.PRESENT)
        m.content = (V, self._membership)
        self._channel.broadcast(m)

    def schedule_broadcast(self, V):
        if self.clock <= V:
            if self._protocol == self.PERIODIC_BROADCAST_PROTOCOL:
                print(f'Send check in present message, id={self.id}')
                self.broadcast_present_msg(V)
                self._check_member_timer = Timer(self._channel.broadcast_delay + self._max_clock_sync_error,
                                                 self._check_membership)
                self._check_member_timer.start()
                self._check_timer = Timer(self._check_in_period, self.schedule_broadcast,
                                          args=[V + datetime.timedelta(seconds=self._check_in_period)])
                self._check_timer.start()
            elif self._protocol == self.ATTENDANCE_LIST_PROTOCOL:
                self._cancel_all_timer()
                sorted_members = sorted([*self._membership])
                pos = sorted_members.index(self.id)
                if pos == 0:
                    # The processor is the one send the attendance list
                    m = self._channel.create_message(self, Message.ATTENDANCE_LIST)
                    m.receiver = self._channel.find_processor(sorted_members[1 % len(sorted_members)])
                    self._channel.send_message(m)
                    pos = len(sorted_members)

                self._check_member_timer = Timer(pos * self._channel.datagram_delay,
                                                 self._check_attendance_list)
                self._check_member_timer.start()
                self._check_timer = Timer(self._check_in_period, self.schedule_broadcast,
                                          args=[V + datetime.timedelta(seconds=self._check_in_period)])
                self._check_timer.start()

    def _check_attendance_list(self):
        if not self._attendance_list_checked:
            print('attendance check failed, init join')
            self.init_join()
        else:
            self._attendance_list_checked = False

    def receive(self, msg):
        """Handles the message receiving based on message type."""
        if msg.type == Message.NEW_GROUP:
            self._handle_new_group_msg(msg)
        elif msg.type == Message.PRESENT:
            self._handle_present_msg(msg)
        elif msg.type == Message.ATTENDANCE_LIST:
            self._handle_attendance_list_msg(msg)
        return

    def crash(self):
        """Crashes this processor, all timer will be stopped"""
        self._status = Processor.CRASHED
        self._current_group = 0
        self._membership = set()
        self._check_in_ids_count = set()
        if self._check_timer is not None:
            self._check_timer.cancel()
        if self._check_member_timer is not None:
            self._check_member_timer.cancel()

    def _cancel_all_timer(self):
        if self._check_timer is not None:
            self._check_timer.cancel()
        if self._check_member_timer is not None:
            self._check_member_timer.cancel()

    def _check_membership(self):
        self._check_in_ids_count.add(self.id)
        if self._check_in_ids_count != self._membership:
            self._check_in_ids_count = set()
            self.init_join()
        self._check_in_ids_count = set()

    def _handle_new_group_msg(self, msg):
        if self.clock > msg.content:
            # the message is outdated
            return
        if self._check_timer is not None:
            self._check_timer.cancel()
        if self._check_member_timer is not None:
            self._check_member_timer.cancel()
        sender_id = msg.sender.id
        self._membership = {self.id, sender_id}
        V = msg.content
        self.broadcast_present_msg(V)
        self._check_timer = Timer(self._check_in_period, self.schedule_broadcast,
                                  args=[V + datetime.timedelta(seconds=self._check_in_period)])
        self._check_timer.start()

    def _handle_present_msg(self, msg):
        V, sender_ids = msg.content
        if sender_ids != self._membership:
            self._membership = sender_ids
            self._membership.add(self.id)
            self._current_group = V
            self._check_in_ids_count = set()
        else:
            self._check_in_ids_count.add(msg.sender.id)

    def _handle_attendance_list_msg(self, msg):
        self._attendance_list_checked = True
        sorted_members = sorted(self.members)
        pos = sorted_members.index(self.id)
        receiver_id = sorted_members[(pos + 1) % len(sorted_members)]
        msg.receiver = self._channel.find_processor(receiver_id)
        print(
            f'id={self.id} receive attendance list msg from {msg.sender.id} '
            f'send attendance list msg to {msg.receiver.id}')
        self._channel.send_message(msg)

    def _compute_time_diff(self, V):
        diff = V.timestamp() + self._check_in_period - self.clock.timestamp()
        return diff

    """Class properties"""

    @property
    def id(self):
        """Returns the id of this processor"""
        return self._id

    @property
    def group(self):
        """Returns the current group of this processor"""
        return self._current_group

    @group.setter
    def group(self, new_group):
        assert type(new_group) == str
        self._current_group = new_group

    @property
    def status(self):
        """Returns the current status of this processor"""
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    @property
    def members(self):
        return [*self._membership]

    @property
    def clock(self):
        """Returns the clock reading of this Processor

        The reading is computed as H(t)+A where H(t) is the standard time in current time zone
        """
        now = time.time()
        tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        return datetime.datetime.fromtimestamp(now + self._clock_diff, tz=tz)

    def __eq__(self, other):
        if type(other) == Processor:
            return other.id == self.id
        return False

    def __str__(self):
        return f'Processor {self.id}, group members: {self.members}'
