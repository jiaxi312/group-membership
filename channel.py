import datetime
import random
import time

from message import Message
from processor import Processor
from threading import Timer


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

    def create_message(self, processor, msg_type):
        """Creates a message in this channel

        Returns:
            A Message object with given sending Processor
        """
        self._assert_processor_registered(processor)
        m = Message(processor, self, msg_type)
        return m

    @staticmethod
    def _send_message_to(message, processor):
        processor.receive(message)

    def send_message(self, message):
        self._assert_processor_registered(message.receiver)
        if message.receiver.status == Processor.CRASHED:
            return
        delay = random.random() * self._datagram_delay
        t = Timer(delay, self._send_message_to, args=(message, message.receiver))
        t.start()

    def broadcast(self, message):
        """Broadcasts the message to all correct processors registered in this channel. """
        if message.sender.status == Processor.CRASHED:
            return
        all_correct_processors = (p for p in self._all_processors if
                                  p.status == Processor.NORMAL and p != message.sender)
        for processor in all_correct_processors:
            delay = random.random() * self._broadcast_delay
            t = Timer(delay, self._send_message_to, args=(message, processor))
            t.start()

    def close(self):
        for processor in self._all_processors:
            processor.crash()
            del processor
        del self

    def find_processor(self, processor_id):
        for processor in self.processors:
            if processor.id == processor_id:
                return processor
        return None

    def _assert_processor_registered(self, processor):
        assert processor in self._all_processors, f"Processor(id={processor.id}) not registered in this channel"

    @property
    def broadcast_delay(self):
        return self._broadcast_delay

    @property
    def datagram_delay(self):
        return self._datagram_delay

    @property
    def processors(self):
        return self._all_processors

    def __contains__(self, item):
        return item in self._all_processors
