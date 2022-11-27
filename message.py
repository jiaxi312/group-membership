class Message:
    """Message class that can broadcast a message or send a datagram message

    A Message represents the basic communication chip in the membership system.
    Processors can broadcast a message to all correct processors or send a message to a given processor.

    Attributes:
        _message_id: A int represents the id of this message
        _sender: A Processor represents the Processor sending the message.
        _receiver: A Processor represents the Processor receiving the message, it could be None if the message
                   is intended for broadcasting.
        _channel: A Channel represents the channel that the message will be delivered through
        _msg_type: A int represents the type of this message
    """

    NEW_GROUP = 1
    ATTENDANCE_LIST = 2
    PRESENT = 3
    ID_COUNT = 0

    def __init__(self, sender, channel, msg_type=NEW_GROUP):
        self._message_id = Message.ID_COUNT
        self._sender = sender
        self._receiver = None
        self._channel = channel
        self._msg_type = msg_type
        self._content = None

        Message.ID_COUNT += 1

    @property
    def id(self):
        return self._message_id

    @property
    def sender(self):
        return self._sender

    @property
    def type(self):
        return self._msg_type

    @property
    def receiver(self):
        return self._receiver

    @receiver.setter
    def receiver(self, new_receiver):
        self._receiver = new_receiver

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content):
        self._content = new_content

    def __str__(self):
        return f'msg: {self.id}, type: {self.type}, sender: {self.sender.id}, content: {self.content}'

    def __eq__(self, other):
        if type(other) == Message:
            return other.id == self.id
        return False

    def __hash__(self):
        return hash(self.id)
