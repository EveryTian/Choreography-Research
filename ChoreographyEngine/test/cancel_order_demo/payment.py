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
listen_port: int = 8005
entity_type: str = 'Payment'
machine_name: str = entity_type
entity_default_data: dict = {}
messages_to_receive: dict = {
    'PaymentCancel': (
        lambda _0, _1: None,
        (
            ['PaymentCancel'],
            lambda _: True,
            [
                ('OrderPaymentUndone', lambda entity_id, _: [entity_id], lambda _: {})
            ]
        )
    )
}
