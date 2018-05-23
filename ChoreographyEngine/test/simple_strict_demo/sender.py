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
whiteboard_address: str = 'http://127.0.0.1'

# Private Part
listen_port: int = 8002
entity_type: str = 'Sender'
machine_name: str = entity_type
entity_default_data: dict = {}
messages_to_receive: dict = {
    'SIG': (
        lambda message_data, entity_data: None,
        (
            ['', 'SIG'],
            lambda entity_data: True,
            [
                ('MSG', lambda entity_id, entity_data: [entity_id], lambda entity_data: {})
            ]
        )
    ),
    'REC': (
        lambda message_data, entity_data: None,
        (
            ['', 'SIG', 'REC'],
            lambda entity_data: True,
            [
                ('ACK', lambda entity_id, entity_data: [entity_id], lambda entity_data: {})
            ]
        )
    )
}
