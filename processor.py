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
    """

    NORMAL = 1
    CRASHED = -1

    def __init__(self, id, channel, max_clock_sync_error, check_in_period):
        """ Inits the Processor with given max clock synchronization error """
        self._id = id
        self._status = Processor.NORMAL
        self._membership = {self.id}
        self._channel = channel
        self._clock_diff = (random.random() - 0.5) * max_clock_sync_error
        self._check_timer = None
        self._check_in_period = check_in_period
        self._current_group = 0

    def init_join(self, broadcast_delay):
        """Initializes the join process, broadcasting the new-group message to all correct processors."""
        self._current_group = self.clock
        self._membership = {self.id}
        m = self._channel.create_message(self, Message.NEW_GROUP)
        m.content = self.clock + datetime.timedelta(seconds=broadcast_delay)
        self._channel.broadcast(m)

    def send(self, target):
        """Sends the given message to target processor"""
        m = self._channel.create_message(self)
        m.receiver = target
        self._channel.send_message(m)

    def broadcast_present_msg(self):
        """Broadcasts the present message to all correct processors"""
        m = self._channel.create_message(self, Message.PRESENT)
        m.content = (self.group, self._membership)
        self._channel.broadcast(m)

    def broadcast(self, V):
        if self.clock <= V:
            self.broadcast_present_msg()
            delay = self._compute_time_diff(V)
            self._check_timer = Timer(delay, self.broadcast_present_msg)
            self._check_timer.start()

    def receive(self, msg):
        """Handles the message receiving based on message type."""
        print(f'processor: {self.id} receives message {msg}')
        if msg.type == Message.NEW_GROUP:
            self._handle_new_group_msg(msg)
        elif msg.type == Message.PRESENT:
            self._handle_present_msg(msg)
        return

    def _handle_new_group_msg(self, msg):
        if self.clock > msg.content:
            # the message is out dated
            return
        if self._check_timer is not None:
            self._check_timer.cancel()

        V = msg.content
        self.broadcast(V)

    def _handle_present_msg(self, msg):
        V, sender_ids = msg.content
        if sender_ids != self._membership:
            self._membership = sender_ids
            self._membership.add(self.id)
            self._current_group = V

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
        return f'Processor {self.id}, group: {self.group}, clock diff: {self._clock_diff}'
