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
    m = Message(1)
    print(m.sender)


if __name__ == '__main__':
    main()
