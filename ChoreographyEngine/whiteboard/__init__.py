#! python3
# coding: utf-8

import json
from threading import Thread
from enum import Enum
from datetime import datetime


class WriterType(Enum):
    SENDER = 'SENDER'
    RECEIVER = 'RECEIVER'


class InvalidWhiteBoardMessageException(Exception):
    pass


class WhiteboardMessage:

    @staticmethod
    def create_from_fields(timestamp: float, writer_type: WriterType, artifact_id: int, message_type: str,
                           from_entity_type: str, from_entity_id: int, to_entities_type: str, to_entities_ids: list):
        if type(writer_type) is not WriterType:
            raise InvalidWhiteBoardMessageException("`%s` is not `WriterType`." % str(writer_type))
        whiteboard_message = WhiteboardMessage()
        whiteboard_message.__timestamp = timestamp
        whiteboard_message.__writer_type = writer_type.value
        whiteboard_message.__artifact_id = artifact_id
        whiteboard_message.__message_type = message_type
        whiteboard_message.__from_entity_type = from_entity_type
        whiteboard_message.__from_entity_id = from_entity_id
        whiteboard_message.__to_entities_type = to_entities_type
        whiteboard_message.__to_entities_ids = to_entities_ids
        whiteboard_message.__generate_data()
        return whiteboard_message

    @staticmethod
    def create_from_message(message_data):
        return WhiteboardMessage(message_data)

    def __init__(self, message_data=None):
        if message_data is None:
            return
        if type(message_data) is str:
            try:
                json_data = json.loads(message_data)
            except json.JSONDecodeError:
                raise InvalidWhiteBoardMessageException("Can not decode `%s`." % message_data)
        elif type(message_data) is dict:
            json_data = message_data
        else:
            raise InvalidWhiteBoardMessageException('Illegal input.')
        try:
            self.__timestamp = json_data['timestamp']
            self.__writer_type = json_data['writer_type']
            self.__artifact_id = json_data['artifact_id']
            self.__message_type = json_data['message_type']
            self.__from_entity_type = json_data['from_entity']['type']
            self.__to_entities_type = json_data['to_entities']['type']
            self.__from_entity_id = json_data['from_entity']['id']
            self.__to_entities_ids = json_data['to_entities']['ids']
        except AttributeError:
            raise InvalidWhiteBoardMessageException('Illegal format.')
        self.__generate_data()

    def __str__(self):
        if self.__writer_type == WriterType.SENDER.value:
            return "%s #%d %s[%d] SENDS %s TO %s%s" % (
                self.time_string, self.__artifact_id, self.__from_entity_type, self.__from_entity_id,
                self.__message_type, self.__to_entities_type, str(self.__to_entities_ids)
            )
        elif self.__writer_type == WriterType.RECEIVER.value:
            return "%s #%d %s%s RECEIVES %s FROM %s[%d]" % (
                self.time_string, self.__artifact_id, self.__to_entities_type, str(self.__to_entities_ids),
                self.__message_type, self.__from_entity_type, self.__from_entity_id
            )
        else:
            return ''

    __repr__ = __str__

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    @property
    def time_string(self) -> str:
        datetime_obj = datetime.fromtimestamp(self.__timestamp)
        return "%d:%d:%d.%d" % (
            datetime_obj.hour, datetime_obj.minute, datetime_obj.second, datetime_obj.microsecond
        )

    @property
    def date_string(self) -> str:
        datetime_obj = datetime.fromtimestamp(self.__timestamp)
        return "%d/%d/%d" % (
            datetime_obj.year, datetime_obj.month, datetime_obj.day
        )

    @property
    def datetime_string(self) -> str:
        datetime_obj = datetime.fromtimestamp(self.__timestamp)
        return "%d/%d/%d-%d:%d:%d.%d" % (
            datetime_obj.year, datetime_obj.month, datetime_obj.day,
            datetime_obj.hour, datetime_obj.minute, datetime_obj.second, datetime_obj.microsecond
        )

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
            'timestamp': self.__timestamp,
            'writer_type': self.__writer_type,
            'artifact_id': self.__artifact_id,
            'message_type': self.__message_type,
            'from_entity': {
                'type': self.__from_entity_type,
                'id': self.__from_entity_id
            },
            'to_entities': {
                'type': self.__to_entities_type,
                'ids': self.__to_entities_ids
            }
        }
        self.__str_data = json.dumps(self.__json_data)


def write_whiteboard(whiteboard_address: str, whiteboard_message):
    from requests import post
    Thread(target=lambda _=None: post(whiteboard_address, json=whiteboard_message.get_json_data()) and None).start()
