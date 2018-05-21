#! python3
# coding: utf-8

import json
from threading import Thread
from requests import post


class WriterType:
    SENDER = 'SENDER'
    RECEIVER = 'RECEIVER'


class InvalidWhiteBoardMessageException(Exception):
    pass


class WhiteboardMessage:

    def __init__(self, writer_type: str, artifact_id: int, message_type: str, 
        from_entity_type: str, from_entity_id: int, to_entities_type: str, to_entities_ids: list):
        self.__writer_type = writer_type
        self.__artifact_id = artifact_id
        self.__message_type = message_type
        self.__from_entity_type = from_entity_type
        self.__from_entity_id = from_entity_id
        self.__to_entities_type = to_entities_type
        self.__to_entities_ids = to_entities_ids
        self.__generate_data()
    
    def __init__(self, message_data):
        json_data: dict
        if type(message_data) is str:
            try:
                json_data = json.loads(message_data)
            except json.JSONDecodeError:
                raise InvalidWhiteBoardMessageException('Can not decode `%s`.' % message_data)
        elif type(message_data) is dict:
            json_data = message_data
        else:
            raise InvalidWhiteBoardMessageException('Illegal input.')
        try:
            self.__writer_type = json_data['writer_type']
            self.__artifact_id = json_data['artifact_id']
            self.__message_type = json_data['message_type']
            self.__from_entity_type = json_data['from_entity']['type']
            self.__to_entities_type = ['to_entities']['type']
            self.__from_entity_id = json_data['from_entity']['id']
            self.__to_entities_ids = ['to_entities']['ids']
        except AttributeError:
            raise InvalidWhiteBoardMessageException('Illegal format.')
        self.__generate_data()

    def __str__(self):
        if self.__writer_type == WriterType.SENDER:
            return "#%d %s[%d] SENDS %s TO %s%s" % (
                self.__artifact_id, self.__from_entity_type, self.__from_entity_id, 
                self.__message_type, self.__to_entities_type, str(self.__to_entities_ids))
        elif self.__writer_type == WriterType.RECEIVER:
            return "#%d %s[%d] RECEIVES %s FROM %s[%d]" % (
                self.__artifact_id, self.__to_entities_type, self.__to_entities_ids[0],
                self.__message_type, self.__from_entity_type, self.__from_entity_id)

    __repr__ = __str__

    @property
    def writer_type(self) -> str:
        return self.__writer_type

    @property
    def artifact_id(self) -> int:
        return self.__artifact_id

    @property
    def message_type(self) -> str:
        return self.__message_type

    @property
    def from_entity_type(self):
        return self.__from_entity_type

    @property
    def from_entity_id(self):
        return self.__from_entity_id

    @property
    def to_entities_type(self):
        return self.__to_entities_type

    @property
    def to_entities_ids(self):
        return self.__to_entities_ids

    def get_json_data(self):
        return self.__json_data

    def get_str_data(self):
        return self.__str_data

    def __generate_data(self):
        self.__json_data = {
            'writer_type': self.__writer_type,
            'artifact_id': self.__artifact_id,
            'message_type': self.__message_type,
            'from_entity': {
                'type': self.__from_entity_type,
                'id': self.__from_entity_id
            },
            'to_entities': {
                'type': self.__to_entity_type,
                'ids': self.__to_entity_ids
            }
        }
        self.__str_data = json.dumps(self.__json_data)
        

def write_whiteboard(whiteboard_address: str, whiteboard_message):
    Thread(target=(lambda _=None: post(whiteboard_address, json=whiteboard_message.get_json_data()))).start()
