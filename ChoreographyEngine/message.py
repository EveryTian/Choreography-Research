#! python3
# coding: utf-8

import sys
from importlib import import_module
from threading import Thread
import json
from requests import post

if len(sys.argv) == 2:
    setting = import_module(sys.argv[1])
else:
    setting = import_module('setting')


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
            response = post(address, json=self.__data, timeout=10)
            print('[R]', response, response.text)

        Thread(target=post_thread_target).start()
