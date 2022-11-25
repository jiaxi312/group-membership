from channel import Channel
from message import Message
from processor import Processor
import datetime
import time


def main():
    broadcast_delay, datagram_delay = 5, 5
    c = Channel(broadcast_delay, datagram_delay)
    p1 = Processor(1, c, 10)
    p2 = Processor(2, c, 10)
    p3 = Processor(3, c, 10)
    c.register_processor(p1)
    c.register_processor(p2)
    c.register_processor(p3)
    p1.init_join(broadcast_delay)
    p2.init_join(broadcast_delay)
    p3.init_join(broadcast_delay)
    now = datetime.datetime.now()
    print(f'current time: {now}')
    time.sleep(10)
    print(p1)
    print(p2)
    print(p3)


if __name__ == '__main__':
    main()
