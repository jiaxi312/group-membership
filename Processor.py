class Processor:
    """A class represents a single Processor in the membership system

    A Processor represents the abstract concept of Processor or Server in Cristian’s
    "Reaching Agreement on Processor Group Membership in Synchronous Distributed Systems" paper.
    A Processor can send a direct message to other processor or broadcast to all correct processors. It also keeps track
    of its status, its view of the membership of group T

    Attributes:
        _current_group: A int indicating the current group the processor belongs to
        _status: A boolean indicating if the processor is
    """

    NORMAL = 1
    CRASHED = -1

    def __init__(self):
        self._current_group = None
        self._status = NORMAL
