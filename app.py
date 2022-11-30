from channel import Channel
from processor import Processor

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
properties = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all-processors')
def get_all_processors():
    data = []
    for processor in properties['channel'].processors:
        status = 'Normal' if processor.status == Processor.NORMAL else 'Crashed'
        data.append({'id': processor.id, 'status': status, 'members': processor.members})
    return jsonify(data), 200


@app.route('/join')
def init_join_for_all_processors():
    for processor in properties['channel'].processors:
        processor.init_join()
    return '', 200


@app.route('/init', methods=['POST'])
def init_processors():
    data = request.json
    for key, value in data.items():
        data[key] = int(value)
    setup(data)
    init_join_for_all_processors()
    return '', 200


@app.route('/crash', methods=['POST'])
def crash_processor():
    data = request.json
    processor_id = int(data['processor_id'])
    processor = properties['channel'].find_processor(processor_id)
    if processor is None:
        return 'Invalid Processor', 404
    processor.crash()
    return '', 200


def setup(kwargs):
    if 'channel' in properties:
        properties['channel'].close()

    properties.update(kwargs)
    channel = Channel(properties['broadcast_delay'], properties['datagram_delay'])
    for _ in range(int(properties['num_processors'])):
        p = Processor(channel, properties['max_clock_sync_error'], properties['check_in_period'])
        channel.register_processor(p)
    properties['channel'] = channel


if __name__ == '__main__':
    app.run(debug=True)
