#! python3
# coding: utf-8

import setting
from flask import Flask, request
from message import Message
from entity import Entity


artifacts: dict = {}


def listen():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def listen():
        handle_message(Message(request.get_json()))
        return setting.machine_name + ' HANDLED'

    app.run(port=setting.listen_port)


def handle_message(message: Message):
    artifact_id = message.get_artifact_id()
    if artifact_id not in artifacts:
        artifacts[artifact_id] = []
    artifact = artifacts[artifact_id]
    # message.
    # Entity(artifact_id, machine_name, artifact_)
