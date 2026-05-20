# tests/schemas/schemas.py - JSON Schema definitions for all API responses

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id":     {"type": "integer"},
        "title":  {"type": "string", "minLength": 1},
        "body":   {"type": "string", "minLength": 1},
    },
    "additionalProperties": False,
}

POST_LIST_SCHEMA = {
    "type": "array",
    "items": POST_SCHEMA,
    "minItems": 1,
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id":       {"type": "integer"},
        "name":     {"type": "string", "minLength": 1},
        "username": {"type": "string", "minLength": 1},
        "email":    {"type": "string", "pattern": r"^[^@]+@[^@]+\.[^@]+$"},
        "phone":    {"type": "string"},
        "website":  {"type": "string"},
        "address": {
            "type": "object",
            "required": ["street", "suite", "city", "zipcode", "geo"],
            "properties": {
                "street":  {"type": "string"},
                "suite":   {"type": "string"},
                "city":    {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "required": ["lat", "lng"],
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"},
                    },
                },
            },
        },
        "company": {
            "type": "object",
            "required": ["name", "catchPhrase", "bs"],
            "properties": {
                "name":        {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs":          {"type": "string"},
            },
        },
    },
}

COMMENT_SCHEMA = {
    "type": "object",
    "required": ["postId", "id", "name", "email", "body"],
    "properties": {
        "postId": {"type": "integer"},
        "id":     {"type": "integer"},
        "name":   {"type": "string", "minLength": 1},
        "email":  {"type": "string", "pattern": r"^[^@]+@[^@]+\.[^@]+$"},
        "body":   {"type": "string", "minLength": 1},
    },
    "additionalProperties": False,
}

TODO_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "completed"],
    "properties": {
        "userId":    {"type": "integer"},
        "id":        {"type": "integer"},
        "title":     {"type": "string"},
        "completed": {"type": "boolean"},
    },
    "additionalProperties": False,
}

CREATED_POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "title", "body", "id"],
    "properties": {
        "userId": {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "id":     {"type": "integer"},
    },
}
