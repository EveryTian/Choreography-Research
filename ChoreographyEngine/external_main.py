#! python3
# coding: utf-8

from threading import Thread
import sys
import json
import main
from message import MessageHandler

new_artifact_id: int = 1
begin_message_type: str
external_type: str = main.setting.entity_type
begin_message_to_entities_type: str
to_entities_ids_chooser: main.function_type


def init_check():
    global begin_message_type
    global begin_message_to_entities_type
    global to_entities_ids_chooser
    try:
        begin_message_type = main.setting.begin_message
    except NameError:
        sys.stderr.write('Error: `begin_message` is not defined.\n')
        return False
    try:
        to_entities_ids_chooser = main.setting.begin_message_to_entities_ids_chooser
    except NameError:
        sys.stderr.write('Error: `begin_message_to_entities_ids_chooser` is not defined.\n')
        return False
    if begin_message_type not in main.setting.messages_paths:
        sys.stderr.write("Error: No message `%s` in `messages_paths`.\n" % begin_message_type)
        return False
    (begin_message_from_entity_type, begin_message_to_entities_type) = main.setting.messages_paths[begin_message_type]
    if begin_message_from_entity_type != external_type:
        sys.stderr.write("Error: Message `%s` not from `%s`.\n" % (begin_message_type, external_type))
        return False
    return True


def send_message(send_data):
    global new_artifact_id
    to_entities_ids = to_entities_ids_chooser(new_artifact_id, send_data)
    MessageHandler(new_artifact_id, begin_message_type,
                   external_type, 1, begin_message_to_entities_type, to_entities_ids, send_data).send()
    new_artifact_id += 1


if __name__ == '__main__' and main.check_setting() and init_check():
    Thread(target=main.listen).start()
    print('Please input the data of the message after `>> `:')
    while True:
        data_str = input('>> ')
        if data_str == 'exit':
            print('Bye!')
            break
        data = {}
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            sys.stderr.write("Error: Cannot decode `%s`.\n" % data_str)
            continue
        if type(data) is not dict:
            sys.stderr.write("Error: Decode result `%s` is not a dict.\n" % str(data))
            continue
        send_message(data)
