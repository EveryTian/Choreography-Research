# Choreography Engine

![ENGINE - NOT TEST](https://img.shields.io/badge/ENGINE-NOT%20TEST-orange.svg)

## Environment

```shell
$ python --version
Python 3.6.5 :: Anaconda custom (64-bit)
```

```python
>>> flask.__version__
'0.12.2'
>>> requests.__version__
'2.18.4'
```

## How to Use

### Run the Engine

- Default: (Use `setting.py` as the config file.)

  ```shell
  $ python main.py # Or you can change the name of `main.py`.
  ```

- Use `some-folder/another-folder/some-file.py` as the config file:

  ```shell
  $ python main.py some-folder.another-folder.some-file
  ```

  Use `setting.py` as the config file:

  ```shell
  $ python main.py setting
  ```

### Configure the Engine

Configure `setting.py` (Or another file name):

#### Public Part

All the machines in one artifact share the same public part, namely, the following two variables:

```python
messages_paths: dict
machines_addresses: dict
```

- Type

  ````haskell
  messages_paths :: Dict String (String, String)
  machines_address :: Dict String String
  ````

- Content

  ```python
  messages_paths: dict = {
      message_type: (from_entity_type, to_entities_type)
  }
  machines_addresses: dict = {
      machine_name : ip_address
  }
  ```

- Example

  ```python
  messages_paths: dict = {
      'OrderCancel': ('External', 'Order'),
      'ReshippingBack': ('Order', 'External'),
      'CancelPurchase': ('Order', 'Purchase'),
      'CancelFulfillment': ('Order', 'Fulfillment')
  }
  machines_addresses: dict = {
      'Order': '192.168.1.1',
      'Purchase': '192.168.1.2',
      'Fulfillment': '192.168.1.3',
      'Payment': '192.168.1.4'
  }
  ```

#### Private Part

The artifact on each machine:

```python
listen_port: int
entity_type: str
machine_name: str
entity_default_data: dict
messages_to_receive: dict
```

- Type

  ```haskell
  listen_port :: Int
  entity_type :: String
  machine_name :: String
  entity_default_data :: JsonDict
  messages_to_receive :: Dict String (String -> String -> (), ([String], JsonDict -> Bool, [(String, Int -> JsonDict -> [Int], JsonDict -> JsonDict)]))
  ```

- Content

  ```javascript
  listen_port = some_port_number
  entity_type = 'some_entity_type'
  machine_name = entity_type
  entity_default_data = {}
  messages_to_receive = {
      message_type: (
         () => data_handler(message_data, entity_data),
         (
             snapshot_to_meet,    // The business
             entity_data => bool, // to meet
             [(message_type, (entity_id, entity_data) => ids_list, entity_data => send_data)]
         )
      )
  }
  ```

  **Attention: `entity_type` should be equal to `machine_name` .**

- Example

  ```python
  listen_port = 5000
  entity_type = 'Payment'
  machine_name = entity_type
  entity_default_data = {}
  messages_to_receive = {
      'PaymentCancel': (
         payment_cancel_data_handler
         (
             ['PaymentCancel'],
             lambda _: True,
             [('OrderPaymentUndone', payment_cancel_get_to_ids_list, lambda _: {})]
         )
      )
  }
  def payment_cancel_data_handler(message_data, entity_data):
      return
  def payment_cancel_get_to_ids_list(from_entity_id, from_entity_data) -> list:
      pass # This function presents the relationships.
  ```

**Click Here: **[**Message Format and Some Questions**](message_format.md)
