class Message:
    """Message class that can broadcast a message or send a datagram message

    A Message represents the basic communication chip in the membership system.
    Processors can broadcast a message to all correct processors or send a message to a given processor.

    Attributes:
        _sender_id: A int represents the id of the Processor sending the message.
        _receiver_id: A int represents the id of the Processor receiving the message, it could be None if the message
                      is intended for broadcasting.
    """

    def __init__(self, sender_id):
        self._sender_id = sender_id
        self._receiver_id = None

    def broadcast(self):
        """Broadcasts this message"""
        raise NotImplementedError("Communication System is not implemented yet")

    def send(self, receiver_id):
        """Sends the datagram message to given Processor id"""
        self._receiver_id = receiver_id
        raise NotImplementedError("Communication System is not implemented yet")

    @property
    def sender(self):
        return self._sender_id

    @property
    def receiver(self):
        return self._receiver_id
