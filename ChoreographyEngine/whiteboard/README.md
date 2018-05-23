# Whiteboard

The whiteboard of the Choreography Engine.

[![TEST - PASS](https://img.shields.io/badge/DEMO%20TEST-PASS-green.svg "Click to See the Sample")](../test/simple_strict_demo)

## How to Use

```shell
$ python whiteboard_main.py <port number> # Or another name
```

- `flask` is required.

  Use `pip install flask` or `conda install flask` to install `flask`.

- If port number is not described, **80** will be used as the default port.

  **Please ensure the port number here is the same with config files in the artifact.**

## Whiteboard Message Format

```json
{
    "timestamp": "timestamp :: number",
    "writer_type": "SENDER / RECEIVER :: string",
    "artifact_id": "artifact_id :: number",
    "message_type": "some_message_type :: string",
    "from_entity": {
        "type": "some_entity_type :: string",
        "id": "entity_id :: number"
    },
    "to_entities": {
        "type": "some_entity_type :: string",
        "ids": [
            "entity_id :: number"
        ]
    }
}
```

## Change Whiteboard Action

You can simply change the action of the whiteboard.

The action function is defined as `whiteboard_handler(whiteboard_message)` .

The current whiteboard handler:

```python
def whiteboard_handler(whiteboard_message):
    print(str(whiteboard_message))
```

*Rewrite the handler to create a different whiteboard.*

You may need `whiteboard_messages` , which stores all the whiteboard messages received. For artifact `#n` , you can find its messages in `whiteboard_messages[n]` .
