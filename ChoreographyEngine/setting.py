# Public Part
messages_paths: dict = {
    # message_type: (from_entity_type, to_entities_type)
}
machines_addresses: dict = {
    # machine_name : ip_address
}

# Private Part
listen_port: int = 5000
entity_type: str = 'some_entity_type'
machine_name: str = entity_type
entity_default_data: dict = {}
messages_to_receive: dict = {
    # message_type: (
    #    message_handler(message_data, entity_data) : function,
    #    (
    #        snapshot : list, entity_data => bool : function, # The business rules to meet
    #        [(message_type : string, (entity_id, entity_data) => [id : number], entity_data => send_data: function)]
    #    )
    # )
}

# For External
begin_message: str = ''


def begin_message_to_entities_ids_chooser():  # Need 2 arguments: entity_id, entity_data
    pass
