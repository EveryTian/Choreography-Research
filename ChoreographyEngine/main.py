#! python3
# coding: utf-8

import sys
import os
from importlib import import_module
from threading import Thread
from time import time
from flask import Flask, request
from utils.typechecker import function_type, check_type
from message import Message
from entity import Entity
import whiteboard

setting_module_name: str = 'setting'
if len(sys.argv) == 2:
    setting_module_name = sys.argv[1]
try:
    setting = import_module(setting_module_name)
except ModuleNotFoundError:
    sys.stderr.write("Error: Config file `%s.py` not found.\n" % os.path.join(*setting_module_name.split('.')))
    sys.exit()

whiteboard_address: str = ''
artifacts: dict = {}


def listen():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def listen_handler():
        message = Message(request.get_json())
        message_type = message.get_message_type()
        artifact_id = message.get_artifact_id()
        from_entity_id = message.get_from_entity_id()
        to_entities_ids = message.get_to_entities_ids()
        if whiteboard_address != '':
            whiteboard.write_whiteboard(whiteboard_address, whiteboard.WhiteboardMessage.create_from_fields(
                time(), whiteboard.WriterType.RECEIVER, artifact_id, message_type,
                message.get_from_entity_type(), from_entity_id, message.get_to_entities_type(), to_entities_ids
            ))
        message_info = "%s[%d](%d->%s)" % (message_type, artifact_id, from_entity_id, str(to_entities_ids))
        print('[L]', message_info)

        def message_handler():
            handle_message(message)

        Thread(target=message_handler).start()
        return setting.machine_name + '_GOT_' + message_info

    print(" * `%s` - Running on http://0.0.0.0:%d/ (Press CTRL+C to quit)"
          % (setting.entity_type, setting.listen_port))
    app.run(host='0.0.0.0', port=setting.listen_port)


def handle_message(message: Message):
    if message.get_to_entities_type() != setting.entity_type:
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


def check_setting():
    try:
        right_types = [
            ('listen_port', setting.listen_port, int),
            ('entity_type', setting.entity_type, str),
            ('machine_name', setting.machine_name, str),
            ('entity_default_data', setting.entity_default_data, dict),
            ('messages_to_receive', setting.messages_to_receive,
             {str: (function_type, ([str], function_type, [(str, function_type, function_type)]))}),
            ('messages_paths', setting.messages_paths, {str: (str, str)}),
            ('machines_addresses', setting.machines_addresses, {str: str})
        ]
    except AttributeError:
        sys.stderr.write('Config Error: Fields is not fully configured.\n')
        return False
    for (setting_item_name, setting_item, right_type) in right_types:
        if not check_type(setting_item, right_type):
            sys.stderr.write("Config Error: `%s` does not match type `%s`.\n" %
                             (setting_item_name, str(right_type)))
            return False
    if setting.entity_type != setting.machine_name:
        sys.stderr.write("Config Error: `entity_type` is `%s` while `machine_name` is `%s`.\n" %
                         (setting.entity_type, setting.machine_name))
        return False
    if setting.entity_type not in setting.machines_addresses:
        sys.stderr.write("Config Error: `entity_type` `%s` is not in `machine_address` list.\n" %
                         setting.entity_type)
        return False
    for message_to_receive_type in setting.messages_to_receive:
        if message_to_receive_type not in setting.messages_paths or \
                setting.messages_paths[message_to_receive_type][1] != setting.entity_type:
            sys.stderr.write("Config Error: No message `%s` for `%s` to receive in `messages_paths`.\n" %
                             (message_to_receive_type, setting.entity_type))
            return False
        for message_to_send_type in map(lambda x: x[0], setting.messages_to_receive[message_to_receive_type][1][2]):
            if message_to_send_type not in setting.messages_paths or \
                    setting.messages_paths[message_to_send_type][0] != setting.entity_type:
                sys.stderr.write("Config Error: No message `%s` for `%s` to send in `messages_paths`.\n" %
                                 (message_to_send_type, setting.entity_type))
                return False
    try:
        if type(setting.whiteboard_address) is not str:
            sys.stderr.write("Config Error: `%s` is not a string.\n" % setting.whiteboard_address)
            return False
        global whiteboard_address
        whiteboard_address = setting.whiteboard_address
    except AttributeError:
        return True
    return True  # Some setting content isn't been checked, including but not limited to port number and address format.


if __name__ == '__main__' and check_setting():
    listen()
