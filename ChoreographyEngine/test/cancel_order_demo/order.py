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
listen_port: int = 8002
entity_type: str = 'Order'
machine_name: str = entity_type
entity_default_data: dict = {}
messages_to_receive: dict = {
    'OrderCancel': (
        lambda _0, _1: None,
        (
            ['OrderCancel'],
            lambda _: True,
            [
                ('ReshippingBack', lambda entity_id, _: [entity_id], lambda _: {}),
                ('CancelPurchase', lambda entity_id, _: [entity_id], lambda _: {}),
                ('CancelFulfillment', lambda entity_id, _: [entity_id], lambda _: {})
            ]
        )
    ),
    'ShippingUndone': (
        lambda _0, _1: None,
        (
            ['ShippingUndone'],
            lambda _: True,
            [
                ('OrderUndone', lambda entity_id, _: [entity_id], lambda _: {})
            ]
        )
    ),
    'OrderPaymentUndone': (
        lambda _0, _1: None,
        (
            ['OrderPaymentUndone'],
            lambda _: True,
            [
                ('InVoice', lambda entity_id, _: [entity_id], lambda _: {})
            ]
        )
    )
}
