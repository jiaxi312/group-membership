from channel import Channel
from message import Message
from processor import Processor
import datetime
import time


def main():
    broadcast_delay, datagram_delay = 1, 1
    max_clock_sync_error = 1
    c = Channel(broadcast_delay, datagram_delay)
    p1 = Processor(c, max_clock_sync_error, 8, Processor.NEIGHBOR_SURVEILLANCE_PROTOCOL)
    p2 = Processor(c, max_clock_sync_error, 8, Processor.NEIGHBOR_SURVEILLANCE_PROTOCOL)
    p3 = Processor(c, max_clock_sync_error, 8, Processor.NEIGHBOR_SURVEILLANCE_PROTOCOL)
    p4 = Processor(c, max_clock_sync_error, 8, Processor.NEIGHBOR_SURVEILLANCE_PROTOCOL)
    p5 = Processor(c, max_clock_sync_error, 8, Processor.NEIGHBOR_SURVEILLANCE_PROTOCOL)
    # p3.status = Processor.CRASHED
    c.register_processor(p1)
    c.register_processor(p2)
    c.register_processor(p3)
    c.register_processor(p4)
    c.register_processor(p5)

    print(f'------group start time {datetime.datetime.now()}------')
    p1.init_join()
    p2.init_join()
    # time.sleep(5)
    p3.init_join()
    p4.init_join()
    p5.init_join()
    now = datetime.datetime.now()
    # print(f'current time: {now}')
    time.sleep(2 * (broadcast_delay + max_clock_sync_error) + 1)
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print(p5)
    time.sleep(10)
    p4.crash()
    print('p4 has crashed')
    time.sleep(15 + 6)
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print(p5)
    # time.sleep(5)
    # p2.status = Processor.CRASHED
    # print('p2 has crashed')
    # time.sleep(3 * (broadcast_delay + max_clock_sync_error) + 5)
    # print(p1)
    # print(p2)
    # print(p3)
    # print(p4)
    # print(p5)


if __name__ == '__main__':
    main()
    # s1 = {1, 2, 3}
    # s2 = set()
    # s2.update(s1)
    # print(s2)
