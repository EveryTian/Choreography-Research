# Cancel Order Demo

![TEST - PASS](https://img.shields.io/badge/TEST-PASS-green.svg)

This is a simple implementation for the "Cancel Order Artifact".

- One-to-one relationships.
- No complex business rules (No need for entity data).

See more in [Cancel Order](/Research/CancelOrder).

## Business Rules

![Business Rules](/Research/CancelOrder/CancelOrderBussinessRulesInMathJaxForGithub.png)

## Config Content

### Public Part

- Machines Addresses

  ```python
  machines_addresses: dict = {
      'External':    'http://127.0.0.1:8001',
      'Order':       'http://127.0.0.1:8002',
      'Fulfillment': 'http://127.0.0.1:8003',
      'Purchase':    'http://127.0.0.1:8004',
      'Payment':     'http://127.0.0.1:8005'
  }
  ```

- Messages Paths

  ```python
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
  ```

### Private Part

Shown in `.py` files.
