from processor import Processor
import datetime
import time


def main():
    p = Processor(1, 100)
    now = datetime.datetime.now()
    print(now)
    print(p.clock)
    print(p)


if __name__ == '__main__':
    main()
