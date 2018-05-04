# Message Format

Message in JSON:

## Current Message Format

```json
{
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
    },
    "data": "data :: json"
}
```

## Some Questions

```json
{
    "artifact_id": "artifact_id :: number",
    "message_type": "some_message_type :: string",
    "relationships": "??? *1*",
    "from_entity": {
        "type": "some_entity_type :: string",
        "id": "entity_id :: number",
        "relationships": "??? *2*"
    },
    "to_entity_type": "some_entity_type :: string *3*",
    "to_entities *4*": {
        "type": "some_entity_type :: string",
        "ids": [
            "entity_id :: number"
        ]
    },
    "data": "data :: json"
}
```

Question:

1. Where to place `relationships`, at *1* or *2* ?
2. How to present `relationships` ?
3. Contains `to_entity_id` or not, at *3* or *4* ?
