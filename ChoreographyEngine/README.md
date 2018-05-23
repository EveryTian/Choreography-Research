# Choreography Engine

![DEMO TEST - PASS](https://img.shields.io/badge/DEMO%20TEST-PASS-green.svg) ![FULL TEST - NEEDED](https://img.shields.io/badge/FULL%20TEST-NEEDED-orange.svg)

## Environment

```shell
$ python --version
Python 3.6.5 :: Anaconda custom (64-bit)
```

```python
>>> flask.__version__
'1.0.2'
>>> requests.__version__
'2.18.4'
```

You can simply install dependencies with `pip` or `conda` :

```shell
$ # Use one of the following command:
$ pip install -r requirements.txt
$ conda install --yes --file requirements.txt
```

(Have better experience on Linux, MacOS, Cygwin and MSYS.)

## Test Demos

- [Simple Demo](test/simple_demo) (Pass)
- [Simple Strict Demo](test/simple_strict_demo) (Pass)
- [Cancel Order Demo](test/cancel_order_demo) (Pass)

## The Whiteboard

The whiteboard is an optional part for an artifact. It keeps the records and the snapshot for the whole artifact.

Click [here](whiteboard) to see more about the usage.

And you need to configure the engine is you want to use the whiteboard (See [here](#configure-the-engine)).

## How to Use

### Run the Engine

**`root` or `Administrator` permission may be needed.**

- Default: (Use `setting.py` as the config file.)

  ```shell
  $ python main.py # Or you can change the name of `main.py`.
  ```
  
- For External, you can use `external_main.py`:

  ```shell
  $ python external_main.py # Or you can change the name of `external_main.py`.
  ```

  ***Attention:*** *When use `external_main.py`, the name of `main.py` can not be changed.*

- Use `some-folder/another-folder/some-file.py` as the config file:

  ```shell
  $ python main.py some-folder.another-folder.some-file
  ```

  ***Attention:*** *`some-folder/another-folder/some-file.py` should have module structure. Namely, `import some-folder.another-folder.some-file` can be executed properly in Python.*

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
whiteboard_address: str  # Optional (If you want to use the whiteboard, then you shall configure this field.)
```

- Type

  ```haskell
  messages_paths :: Dict String (String, String)
  machines_address :: Dict String String
  whiteboard_address :: String -- Optional
  ```
  ```python
  # For type_checker.py:
  messages_paths_type = {str: (str, str)}
  machines_address_type = {str: str}
  whiteboard_address_type = str  # Optional
  ```

- Content

  ```python
  messages_paths: dict = {
      message_type: (from_entity_type, to_entities_type)
  }
  machines_addresses: dict = {
      machine_name : ip_address
  }
  whiteboard_address: str = 'http://whiteboard.addr'  # Optional
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
      'Order': 'http://192.168.1.1:3000',
      'Purchase': 'http://192.168.1.2',
      'Fulfillment': 'http://192.168.1.3:8000',
      'Payment': 'http://192.168.1.4:80'
  }
  whiteboard_address: str = 'http://192.168.1.5:80'  # Optional
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

And here is an optional part for `External`:

**Only** when use `external_main.py`, you need and shall config the following 2 items:

```python
begin_message: str
begin_message_to_entities_ids_chooser: function
```

- Type

  ```haskell
  listen_port :: Int
  entity_type :: String
  machine_name :: String
  entity_default_data :: JsonDict
  messages_to_receive :: Dict String (String -> String -> (), ([String], JsonDict -> Bool, [(String, Int -> JsonDict -> [Int], JsonDict -> JsonDict)]))
  begin_message :: String
  begin_message_to_entities_ids_chooser :: Int -> JsonDict -> [Int]
  ```
  ```python
  # For type_checker.py:
  listen_port_type = int
  entity_type_type = str
  machine_name_type = str
  entity_default_data_type = dict
  messages_to_receive_type = {str: (function_type, ([str], function_type, [(str, function_type, function_type)]))}
  begin_message_type = str
  begin_message_to_entities_ids_chooser_type = function_type
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
  begin_message_type = 'begin_message_type'
  begin_message_to_entities_ids_chooser_type = (entity_id, entity_data) => ids_list
  ```

  - **Attention 1: `entity_type` should be equal to `machine_name` .**
  
  - **Attention 2: There is a strict mode for `snapshot_to_meet`. In the strict mode, the snapshot meets only if `snapshot_to_meet` is the same as the snapshot in an entity. To enable the strict mode, just make `snapshot_to_meet[0]` the empty string `''`.**

    For example:
    
    - Both `snapshot_to_meet = ['A']` (nonstrict mode) and `snapshot_to_meet = ['A', 'B']` (nonstrict mode) meets the entity snapshot `['A', 'B', 'C']`.
    
    - `snapshot_to_meet = ['A', 'B', 'C', 'D']` (nonstrict mode) does not meet the entity snapshot `['A', 'B', 'C']`.
    
    - `snapshot_to_meet = ['', 'A']` (strict mode), `snapshot_to_meet = ['', 'A', 'B']` (strict mode) and `snapshot_to_meet = ['', 'A', 'B', 'C', 'D']` (strict mode) do not meet the entity snapshot `['A', 'B', 'C']`.
    
    - In the strict mode, only `snapshot_to_meet = ['', 'A', 'B', 'C']` meets the entity snapshot `['A', 'B', 'C']`.

- Example

  ```python
  listen_port = 5000
  entity_type = 'Payment'
  machine_name = entity_type
  entity_default_data = {}
  messages_to_receive = {
      'PaymentCancel': (
         payment_cancel_data_handler,
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

**Click Here:** [**Message Format**](MessageFormat.md)
