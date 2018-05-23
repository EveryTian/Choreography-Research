#! python3
# coding: utf-8

import sys
from flask import Flask, request
from __init__ import WhiteboardMessage

listen_port: int = 80
whiteboard_messages: dict = {}


def whiteboard_handler(whiteboard_message):
    print(str(whiteboard_message))


def listen():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def listen_handler():
        whiteboard_message = WhiteboardMessage(request.get_json())
        artifact_id = whiteboard_message.artifact_id
        if artifact_id not in whiteboard_messages:
            whiteboard_messages[artifact_id] = []
        whiteboard_messages[artifact_id].append(whiteboard_message)
        whiteboard_handler(whiteboard_message)
        return 'Whiteboard handled.'

    print(' * Whiteboard running on http://0.0.0.0:' + str(listen_port) + '/ (Press CTRL+C to quit)')
    app.run(host='0.0.0.0', port=listen_port)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            listen_port = int(sys.argv[1])
        except ValueError:
            sys.stderr.write("Error: `%s` is not a number\n" % str(listen_port))
        sys.exit()
    listen()
