#! python3
# coding: utf-8

import sys
from importlib import import_module
from message import Message, MessageHandler

if len(sys.argv) == 2:
    setting = import_module(sys.argv[1])
else:
    setting = import_module('setting')


class Entity:

    # Here **may** be some static data

    def __init__(self, artifact_id: int, entity_type: str, entity_id: int):
        self.__artifact_id = artifact_id
        self.__entity_type = entity_type
        self.__entity_id = entity_id
        self.__snapshot = {}
        self.__data = setting.entity_default_data
        for message_type in setting.messages_to_receive:
            self.__snapshot[message_type] = False

    def __eq__(self, obj):
        return type(obj) is Entity \
               and self.__artifact_id == obj.__artifact_id \
               and self.__entity_type == obj.__entity_type \
               and self.__entity_id == obj.__entity_id

    def __str__(self):
        return "%s[%d]in(%d)" % (self.__entity_type, self.__entity_id, self.__artifact_id)

    __repr__ = __str__

    def get_artifact_id(self) -> int:
        return self.__artifact_id

    def get_entity_type(self) -> str:
        return self.__entity_type

    def get_entity_id(self) -> int:
        return self.__entity_id

    def get_snapshot(self) -> dict:
        return self.__snapshot

    def get_data(self) -> dict:
        return self.__data

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

    def handle_message(self, message: Message):
        if message.get_artifact_id() != self.__artifact_id:
            return
        message_type = message.get_message_type()
        self.__snapshot[message_type] = True
        (data_handler,
         business_rule) = setting.messages_to_receive[message_type]
        data_handler(message.get_message_data(), self.__data)
        (snapshot_to_meet, logic_rule, messages_to_send) = business_rule
        # TODO: Choose `is_just_messages_got` or `is_messages_got`?
        if self.is_just_messages_got(snapshot_to_meet) and logic_rule(self.__data):
            for (message_type, to_entities_ids_generator, send_data_generator) in messages_to_send:
                (from_entity_type,
                 to_entities_type) = setting.messages_paths[message_type]
                if from_entity_type != setting.entity_type:
                    continue
                to_entities_ids = to_entities_ids_generator(
                    self.__entity_id, self.__data)
                send_data = send_data_generator(self.__data)
                MessageHandler(self.__artifact_id, message_type, from_entity_type,
                               self.__entity_id, to_entities_type, to_entities_ids, send_data).send()
