# Whiteboard

The whiteboard of the Choreography Engine.

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
