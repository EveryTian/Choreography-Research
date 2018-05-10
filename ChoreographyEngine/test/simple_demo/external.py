# Public Part:
messages_paths: dict = {
    'SIG': ('External', 'Sender'),
    'MSG': ('Sender', 'Receiver'),
    'REC': ('Receiver', 'Sender'),
    'ACK': ('Sender', 'External')
}
machines_addresses: dict = {
    'External': 'http://127.0.0.1:8001',
    'Sender': 'http://127.0.0.1:8002',
    'Receiver': 'http://127.0.0.1:8003'
}

# Private Part
listen_port: int = 8001
entity_type: str = 'External'
machine_name: str = entity_type
entity_default_data: dict = {}
messages_to_receive: dict = {
    'ACK': (
        lambda message_data, entity_data: print(message_data, entity_type),
        (
            [], lambda _: False, []  # `lambda _: False` means 'ACK' ends with no messages to be sent out.
        )
    )
}
