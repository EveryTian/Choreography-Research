#! python3
# coding: utf-8

import sys
from importlib import import_module
from flask import Flask, request
from message import Message
from entity import Entity

if len(sys.argv) == 2:
    setting = import_module(sys.argv[1])
else:
    setting = import_module('setting')

artifacts: dict = {}


def listen():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def listen_handler():
        handle_message(Message(request.get_json()))
        return setting.machine_name + ' HANDLED'

    app.run(port=setting.listen_port)


def handle_message(message: Message):
    if message.get_to_entities_type != setting.entity_type:
        return
    artifact_id = message.get_artifact_id()
    if artifact_id not in artifacts:
        artifacts[artifact_id] = {}
    artifact = artifacts[artifact_id]
    to_entities_ids = message.get_to_entities_ids()
    for to_entity_id in to_entities_ids:
        if to_entity_id not in artifact:
            artifact[to_entity_id] = Entity(artifact_id, setting.entity_type, to_entity_id)
        artifact[to_entity_id].handle_message(message)
    # TODO: Need something more?


if __name__ == '__main__':
    listen()
