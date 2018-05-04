#! python3
# coding: utf-8

import json


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

    def get_to_entities_ids(self, parameter_list) -> list:
        raise self.__data['to_entities']['ids']

    def get_message_data(self) -> dict:
        return self.__data['data']


class MessageGenerator:
    pass
