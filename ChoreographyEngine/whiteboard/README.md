# Whiteboard

The whiteboard of the Choreography Engine.

## How to Use

```shell
$ python whiteboard_main.py <port number> # Or another name
```

If port number is not described, 80 will be used as the default port.

**Please ensure the port number here is the same with config files in the artifact.**

## Whiteboard Message Format

**Attention:** When `"writer_type"` is `"RECEIVER"`, `"to_entities"["ids"]` shall and noly shall let `"to_entities"["ids"][0]` the receiver, and need not to provide other entites' ids. Namely, `len("to_entities"["ids"])` shall be greater than or equal to 1 and only `"to_entities"["ids"][0]` makes sense.

```json
{
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
