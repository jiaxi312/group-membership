from channel import Channel
from processor import Processor

from flask import Flask, render_template

app = Flask(__name__)
properties = {'max_clock_sync_error': 1, 'broadcast_delay': 1, 'datagram_delay': 1, 'channel': None,
              'check_in_period': 5}


@app.route('/')
def index():
    setup()
    print(*properties['channel'].processors)
    return render_template('index.html')


@app.route('/all-processors')
def get_all_processors():
    return [str(processor) for processor in properties['channel'].processors]


def setup():
    properties['channel'] = Channel(properties['broadcast_delay'], properties['datagram_delay'])
    for _ in range(3):
        p = Processor(properties['channel'], properties['max_clock_sync_error'], properties['check_in_period'])
        properties['channel'].register_processor(p)


if __name__ == '__main__':
    app.run(debug=True)
