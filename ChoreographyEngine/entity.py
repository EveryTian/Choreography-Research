#! python3
# coding: utf-8

import setting
from message import Message


# class Artifact:
#     def __init__():
#         self.__entities = []


class Entity:

    # Here may be some static data

    def __init__(self, artifact_id: int, entity_type: str, entity_id: int):
        self.__artifact_id = artifact_id
        self.__entity_type = entity_type
        self.__entity_id = entity_id
        self.__snapshot = {}
        for message_type in setting.messages_to_receive:
            self.__snapshot[message_type] = False

    def __eq__(self, obj):
        return type(obj) is Entity and self.__artifact_id == obj.__artifact_id and self.__entity_type == obj.__entity_type and self.__entity_id == obj.__entity_id

    def __str__(self):
        return "%s[%d]in(%d)" % (self.__entity_type, self.__entity_id, self.__artifact_id)

    def __repr__(self):
        return str(self)

    def get_artifact_id(self) -> int:
        return self.__artifact_id

    def get_entity_type(self) -> str:
        return self.__entity_type

    def get_entity_id(self) -> int:
        return self.__entity_id

    def get_snapshot(self) -> dict:
        return self.__snapshot

    def is_messages_got(self, messages_types: list) -> bool:
        for message_type in messages_types:
            if not self.__snapshot[message_type]:
                return False
        return True

    def is_just_messages_got(self, messages_types: list) -> bool:
        for message_type in self.__snapshot:
            if self.__snapshot[message_type]:
                if message_type not in messages_types:
                    return False
            elif message_type in messages_types:
                return False
        return True

    def handleMessage(self, message: Message):
        if message.get_artifact_id() != self.__artifact_id or message.get_to_entity_type != setting.entity_type:
            return
        message_type = message.get_message_type()
        self.__snapshot[message_type] = True
        
