# Public Part:
messages_paths: dict = {
    'OrderCancel':        ('External',    'Order'),
    'ReshippingBack':     ('Order',       'External'),
    'CancelPurchase':     ('Order',       'Purchase'),
    'CancelFulfillment':  ('Order',       'Fulfillment'),
    'PurchaseUndone':     ('Purchase',    'Fulfillment'),
    'ShippingBack':       ('External',    'Fulfillment'),
    'ShippingUndone':     ('Fulfillment', 'Order'),
    'OrderUndone':        ('Order',       'External'),
    'PaymentCancel':      ('External',    'Payment'),
    'OrderPaymentUndone': ('Payment',     'Order'),
    'InVoice':            ('Order',       'External')
}
machines_addresses: dict = {
    'External':    'http://127.0.0.1:8001',
    'Order':       'http://127.0.0.1:8002',
    'Fulfillment': 'http://127.0.0.1:8003',
    'Purchase':    'http://127.0.0.1:8004',
    'Payment':     'http://127.0.0.1:8005'
}

# Private Part
listen_port: int = 8003
entity_type: str = 'Fulfillment'
machine_name: str = entity_type
entity_default_data: dict = {}

fulfillment_messages_receiver = (
        lambda _0, _1: None,
        (
            ['CancelFulfillment', 'PurchaseUndone', 'ShippingBack'],
            lambda _: True,
            [
                ('ShippingUndone', lambda entity_id, _: [entity_id], lambda _: {})
            ]
        )
    )

messages_to_receive: dict = {
    'CancelFulfillment': fulfillment_messages_receiver,
    'PurchaseUndone':    fulfillment_messages_receiver,
    'ShippingBack':      fulfillment_messages_receiver
}
