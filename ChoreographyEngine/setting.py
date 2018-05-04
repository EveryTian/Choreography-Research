listen_port: int = 5000
entity_type: str = 'some_entity_type'
machine_name: str = entity_type
entity_default_data: dict = {}
messages_to_receive: dict = {
    # message_type: (
    #    message_handler(message_data, entity_data) : function,
    #    (
    #        snapshot : list, entity_data => bool : function, # The business rules to meet
    #        [(to_entity_type : string, entity_data => [id : number], entity_data => send_data: function)]
    #    )
    # )
}
machines_addresses = {
    # machine_name : ip_address
}
