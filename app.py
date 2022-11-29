from channel import Channel
from processor import Processor

from flask import Flask, render_template, jsonify, Response

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
    data = []
    for processor in properties['channel'].processors:
        data.append({'id': processor.id, 'members': processor.members})
    print(data)
    return jsonify(data), 200


@app.route('/join')
def init_join_for_all_processors():
    for processor in properties['channel'].processors:
        print(f'Processor {processor.id} init join')
        processor.init_join()
    return '', 200


def setup():
    if properties['channel'] is not None:
        return
    properties['channel'] = Channel(properties['broadcast_delay'], properties['datagram_delay'])
    for _ in range(5):
        p = Processor(properties['channel'], properties['max_clock_sync_error'], properties['check_in_period'])
        properties['channel'].register_processor(p)


if __name__ == '__main__':
    app.run(debug=True)
