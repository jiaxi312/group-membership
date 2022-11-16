from channel import Channel
from message import Message
from processor import Processor
import datetime
import time


def main():
    c = Channel(5, 5)
    p1 = Processor(1, 10)
    p2 = Processor(2, 10)
    p3 = Processor(3, 10)
    c.register_processor(p1)
    c.register_processor(p2)
    m = c.create_message(p1)

    now = datetime.datetime.now()
    print(f'current time: {now}')
    m.send(receiver=p3)


if __name__ == '__main__':
    main()
