from channel import Channel
from message import Message
from processor import Processor
import datetime
import time


def main():
    broadcast_delay, datagram_delay = 5, 5
    max_clock_sync_error = 1
    c = Channel(broadcast_delay, datagram_delay)
    p1 = Processor(1, c, max_clock_sync_error, 10)
    p2 = Processor(2, c, max_clock_sync_error, 10)
    p3 = Processor(3, c, max_clock_sync_error, 10)
    # p3.status = Processor.CRASHED
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
    time.sleep(2 * (broadcast_delay + max_clock_sync_error) + 1)
    print(p1)
    print(p2)
    print(p3)


if __name__ == '__main__':
    main()
