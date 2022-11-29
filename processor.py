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

    def __init__(self, channel, max_clock_sync_error, check_in_period):
        """ Inits the Processor with given max clock synchronization error """
        self._id = Processor.ID_COUNT
        self._current_group = 0
        self._status = Processor.NORMAL
        self._membership = set()
        self._channel = channel
        self._max_clock_sync_error = max_clock_sync_error
        self._clock_diff = (random.random() - 0.5) * max_clock_sync_error
        self._check_timer = None
        self._check_in_period = check_in_period
        self._check_in_ids_count = {}
        Processor.ID_COUNT += 1

    def init_join(self, broadcast_delay):
        """Initializes the join process, broadcasting the new-group message to all correct processors."""
        print(f'processor {self.id} init group')
        # print(f'{self._check_in_ids_count}, {self._membership}')
        self._membership = set()
        m = self._channel.create_message(self, Message.NEW_GROUP)
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
            print(f'Send check in present message, id={self.id}')
            self.broadcast_present_msg(V)
            t = Timer(self._channel.broadcast_delay + self._max_clock_sync_error + 1,
                      self._check_membership)
            t.start()
            self._check_timer = Timer(self._check_in_period, self.schedule_broadcast,
                                      args=[V + datetime.timedelta(seconds=self._check_in_period)])
            self._check_timer.start()

    def periodic_broad_cast_check(self, V):
        self._check_in_ids_count = {self.id}
        self.broadcast_present_msg(V)
        t = Timer(self._channel.broadcast_delay + self._max_clock_sync_error,
                  self._check_membership)
        t.start()

    def _check_membership(self):
        if set(self._check_in_ids_count.keys()) != self._membership:
            self.init_join(self._channel.broadcast_delay)
            return
        count = -1
        for key, value in self._check_in_ids_count.items():
            if key == self.id:
                continue
            elif count == -1:
                count = value
            elif count != value:
                self.init_join(self._channel.broadcast_delay)
                break

    def receive(self, msg):
        """Handles the message receiving based on message type."""
        if msg.type == Message.NEW_GROUP:
            self._handle_new_group_msg(msg)
        elif msg.type == Message.PRESENT:
            self._handle_present_msg(msg)
        return

    def _handle_new_group_msg(self, msg):
        if self.clock > msg.content:
            # the message is outdated
            return
        if self._check_timer is not None:
            self._check_timer.cancel()
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
            self._check_in_ids_count = {id: 0 for id in self._membership}
            self._current_group = V
        elif msg.sender.id in self._check_in_ids_count:
            self._check_in_ids_count[msg.sender.id] += 1

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
