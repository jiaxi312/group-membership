from channel import Channel
from message import Message
from processor import Processor
import datetime
import time


def main():
    p = Processor(1, 100)
    now = datetime.datetime.now()
    print(now)
    print(p.clock)
    print(p)
    c = Channel()
    c.register_processor(p)
    print(3 in c)


if __name__ == '__main__':
    main()
