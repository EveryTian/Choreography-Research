#! python3
# coding: utf-8

import message


class Entity:

    # Here may be some static data

    def __init__(self, artifact_id, entity_type, entity_id):
        self.__artifact_id = artifact_id
        self.__entity_type = entity_type
        self.__entity_id = entity_id

    def __eq__(self, obj):
        return type(obj) is Entity and self.__artifact_id == obj.__artifact_id and self.__entity_type == obj.__entity_type and self.__entity_id == obj.__entity_id

    def __str__(self):
        return "%s[%d]in(%d)" % (self.__entity_type, self.__entity_id, self.__artifact_id)

    def __repr__(self):
        return str(self)

    def get_artifact_id(self):
        return self.__artifact_id

    def get_entity_type(self):
        return self.__entity_type

    def get_entity_id(self):
        return self.__entity_id

    def handleMessage(self, message):
        if message.get_artifact_id() != self.__artifact_id:
            return  # Just do
        pass
