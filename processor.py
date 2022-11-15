class Processor:
    """A class represents a single Processor in the membership system

    A Processor represents the abstract concept of Processor or Server in Cristian’s
    "Reaching Agreement on Processor Group Membership in Synchronous Distributed Systems" paper.
    A Processor can send a direct message to other processor or broadcast to all correct processors. It also keeps track
    of its status, its view of the membership of group T

    Attributes:
        _current_group: A int indicating the current group the processor belongs to
        _status: A int constant indicating the status of the Processor
        _membership: A list contains the Processor's view of its memberships in the _current_group
    """

    NORMAL = 1
    CRASHED = -1

    def __init__(self):
        self._current_group = None
        self._status = Processor.NORMAL
        self._membership = []

    """Class properties"""
    @property
    def group(self):
        return self._current_group

    @group.setter
    def group(self, new_group):
        assert type(new_group) == int
        self._current_group = new_group

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status
