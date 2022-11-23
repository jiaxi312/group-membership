import random
import time
import datetime


class Processor:
    """A class represents a single Processor in the membership system

    A Processor represents the abstract concept of Processor or Server in Cristian’s
    "Reaching Agreement on Processor Group Membership in Synchronous Distributed Systems" paper.
    A Processor can send a direct message to other processor or broadcast to all correct processors. It also keeps track
    of its status, its view of the membership of group T. It may also contain clock synchronization error when
    initialized.

    Attributes:
        _id: A int indicating the id of this Processor
        _current_group: A int indicating the current group the processor belongs to
        _status: A int constant indicating the status of the Processor
        _membership: A list contains the Processor's view of its memberships in the _current_group
        _channel: A Channel object where the processor is attached to
        _clock_diff: A float representing the clock synchronization error of this Processor clock from the master clock
    """

    NORMAL = 1
    CRASHED = -1

    def __init__(self, id, channel, max_clock_sync_error):
        """ Inits the Processor with given max clock synchronization error """
        self._id = id
        self._current_group = None
        self._status = Processor.NORMAL
        self._membership = []
        self._channel = channel
        self._clock_diff = (random.random() - 0.5) * max_clock_sync_error

    def send(self, target):
        """Sends the given message to target processor"""
        m = self._channel.create_message(self)
        m.receiver = target
        self._channel.send_message(m)

    def broadcast(self):
        """Broadcasts the message to all correct processors"""
        raise NotImplementedError

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
        assert type(new_group) == int
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

        The reading is computed as H(t)+A where H(t) is the standard current time
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
