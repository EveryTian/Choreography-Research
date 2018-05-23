#! python3
# coding: utf-8

import sys
import os
from importlib import import_module
from threading import Thread
from time import time
import json
from requests import post
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
try:
    whiteboard_address = setting.whiteboard_address
except AttributeError:
    pass


class Message:

    def __init__(self, data):
        if type(data) is str:
            self.__data_string = data
            self.__data = json.loads(data)
        elif type(data) is dict:
            self.__data = data
            self.__data_string = json.dumps(data)

    def __str__(self):
        return self.__data_string

    def get_data_dict(self) -> dict:
        return self.__data

    def get_data_string(self) -> str:
        return self.__data_string

    def get_artifact_id(self) -> int:
        return self.__data['artifact_id']

    def get_message_type(self) -> str:
        return self.__data['message_type']

    def get_from_entity_type(self) -> str:
        return self.__data['from_entity']['type']

    def get_from_entity_id(self) -> int:
        return self.__data['from_entity']['id']

    def get_to_entities_type(self) -> str:
        return self.__data['to_entities']['type']

    def get_to_entities_ids(self) -> list:
        return self.__data['to_entities']['ids']

    def get_message_data(self) -> dict:
        return self.__data['data']


class MessageHandler:

    def __init__(self, artifact_id: int, message_type: str,
                 from_entity_type: str, from_entity_id: int,
                 to_entities_type: str, to_entities_ids: list, data: dict):
        self.__data = {
            'artifact_id': artifact_id,
            'message_type': message_type,
            'from_entity': {
                'type': from_entity_type,
                'id': from_entity_id
            },
            'to_entities': {
                'type': to_entities_type,
                'ids': to_entities_ids
            },
            'data': data
        }
        self.__artifact_id = artifact_id
        self.__message_type = message_type
        self.__from_entity_type = from_entity_type
        self.__from_entity_id = from_entity_id
        self.__to_entities_type = to_entities_type
        self.__to_entities_ids = to_entities_ids
        self.__to_address = setting.machines_addresses[to_entities_type]

    def __str__(self):
        return 'MessageHandler: ' + str(self.__data)

    __repr__ = __str__

    def get_data_string(self):
        return json.dumps(self.__data)

    def get_data_dict(self):
        return self.__data

    def send(self, address: str = None):
        if address is None or type(address) is not str:
            address = self.__to_address

        def post_thread_target():
            print('[S]', 'Send Message:', self.__data)
            response = post(address, json=self.__data)
            print('[R]', response, response.text)

        if whiteboard_address != '':
            whiteboard.write_whiteboard(whiteboard_address, whiteboard.WhiteboardMessage.create_from_fields(
                time(), whiteboard.WriterType.SENDER, self.__artifact_id, self.__message_type,
                self.__from_entity_type, self.__from_entity_id, self.__to_entities_type, self.__to_entities_ids
            ))
        Thread(target=post_thread_target).start()
