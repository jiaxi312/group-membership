from message import Message
from processor import Processor


class Channel:
    """The system that controls messages transmissions

    Channel serves as the transportation center that direct the message to its intended receiver.
    Channel must be initialized before the creation of processors, and each new processors when created should be
    added to the channel so that it can keep track of all processors.

    Attributes:
        _broadcast_delay: A float represents the upper bound time delay for broadcast
        _datagram_delay: A float represents the upper bound time delay for direct message sending
        _all_processors: A list keeps track of all processors in this channel
        _messages: A list keeps track of all messages being created through this channel
    """

    def __init__(self, broadcast_delay, datagram_delay):
        self._broadcast_delay = broadcast_delay
        self._datagram_delay = datagram_delay
        self._all_processors = []
        self._messages = []

    def register_processor(self, processor):
        """Registers the given processor to the channel

        Returns:
            True if the processor is successfully added, False otherwise.
        """
        if processor in self:
            return False
        self._all_processors.append(processor)
        return False

    def create_message(self, processor: Processor):
        """Creates a message in this channel

        Returns:
            A Message object with given sending Processor
        """
        message_id = len(self._messages)
        m = Message(message_id, processor.id, self)
        self._messages.append(m)
        return m

    def __contains__(self, item):
        return item in self._all_processors
