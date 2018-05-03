#! python3
# coding: utf-8

import json


class Message:
    def __init__(self, data_string):
        self.__origin_data_string = data_string
        self.__data = json.loads(data_string)
    def __str__(self):
        return self.__origin_data_string
    def get_data(self):
        return self.__data
    def get_origin_data_string(self):
        return self.__origin_data_string
    def get_artifact_id(self):
        return self.__data['artifact_id']
    def get_message_type(self):
        return self.__data['message_type']
    def get_from_entity_type(self):
        return self.__data['from_entity']['type']
    def get_from_entity_id(self):
        return self.__data['from_entity']['id']

class MessageGenerator:
    pass
