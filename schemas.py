pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        }
    }
}
order_create = {
    "type": "object",
    "required": ["pet_id"],
    "properties": {
        "pet_id": {"type": "integer"}
    }
}

order_response = {
    "type": "object",
    "required": ["id", "pet_id", "status"],
    "properties": {
        "id": {"type": "string"},
        "pet_id": {"type": "integer"},
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
       }
    }
}



