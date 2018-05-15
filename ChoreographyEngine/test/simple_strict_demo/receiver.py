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
listen_port: int = 8003
entity_type: str = 'Receiver'
machine_name: str = entity_type
entity_default_data: dict = {}
messages_to_receive: dict = {
    'MSG': (
        lambda _0, _1: None,
        (
            ['', 'MSG'],
            lambda _: True,
            [
                ('REC', lambda entity_id, _: [entity_id], lambda _: {})
            ]
        )
    )
}
