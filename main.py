from channel import Channel
from message import Message
from processor import Processor
import datetime
import time


def main():
    broadcast_delay, datagram_delay = 5, 5
    c = Channel(broadcast_delay, datagram_delay)
    p1 = Processor(1, c, 0, 3)
    p2 = Processor(2, c, 0, 3)
    p3 = Processor(3, c, 0, 3)
    c.register_processor(p1)
    c.register_processor(p2)
    c.register_processor(p3)
    print(f'------group start time {datetime.datetime.now()}------')
    p1.init_join(broadcast_delay)
    p2.init_join(broadcast_delay)
    # time.sleep(5)
    p3.init_join(broadcast_delay)
    now = datetime.datetime.now()
    print(f'current time: {now}')
    time.sleep(broadcast_delay + 1)
    print(p1)
    print(p2)
    print(p3)


if __name__ == '__main__':
    main()
