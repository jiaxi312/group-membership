from channel import Channel
from message import Message
from processor import Processor
import datetime
import time


def main():
    c = Channel(5, 5)
    p1 = Processor(1, c, 10)
    p2 = Processor(2, c, 10)
    p3 = Processor(3, c, 10)
    c.register_processor(p1)
    c.register_processor(p2)
    p1.send(p2)
    now = datetime.datetime.now()
    print(f'current time: {now}')


if __name__ == '__main__':
    main()
