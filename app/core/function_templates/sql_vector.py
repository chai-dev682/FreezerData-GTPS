import json

function_list = [
    {
        "type": "function",
        "function": {
            "name": "determine_sql_or_vector",
            "description": "This function is using conversation between user and assistant as input and determine whether using sql is good or using vectordb is good",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_sql": {
                        "type": "string",
                        "enum": ["yes", "no", "unknown"],
                        "description": "If using SQL is good this property returns 'yes', and if using vectordb is good return 'no', and if information is not provided, return 'unknown'"
                    }
                },
                "required": ["is_sql"]
            }
        }
    }
]

sql_vector_tool = json.loads(json.dumps(function_list))