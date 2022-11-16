from channel import Channel


class Message:
    """Message class that can broadcast a message or send a datagram message

    A Message represents the basic communication chip in the membership system.
    Processors can broadcast a message to all correct processors or send a message to a given processor.

    Attributes:
        _message_id: A int represents the id of this message
        _sender_id: A int represents the id of the Processor sending the message.
        _receiver_id: A int represents the id of the Processor receiving the message, it could be None if the message
                      is intended for broadcasting.
        _channel: A Channel represents the channel that the message will be delivered through
    """

    def __init__(self, message_id, sender_id, channel: Channel):
        self._message_id = message_id
        self._sender_id = sender_id
        self._receiver_id = None
        self._channel = channel

    def broadcast(self):
        """Broadcasts this message"""
        raise NotImplementedError("Communication System is not implemented yet")

    def send(self, receiver_id):
        """Sends the datagram message to given Processor id"""
        self._receiver_id = receiver_id
        raise NotImplementedError("Communication System is not implemented yet")

    @property
    def id(self):
        return self._message_id

    @property
    def sender(self):
        return self._sender_id

    @property
    def receiver(self):
        return self._receiver_id
