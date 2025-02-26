import json

function_list = [
    {
        "type": "function",
        "function": {
            "name": "extract_object_id",
            "description": "Extract object ID from user query. Object IDs are typically mentioned as numbers after words like 'object', 'id', 'number', '#', etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_id": {
                        "type": "integer",
                        "description": "The extracted object ID. If no object ID is found, return null"
                    }
                },
                "required": ["object_id"]
            }
        }
    }
]

extract_object_id_tool = json.loads(json.dumps(function_list))