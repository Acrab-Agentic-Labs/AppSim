TASK23_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取周边美食排行榜第一名的名称。",
    "properties": {
        "restaurant_name": {
            "type": "string",
            "description": "美食排行榜第一名的完整名称。",
        }
    },
    "required": ["restaurant_name"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("restaurant_name") or "")
    return "Smile and Salad" in name
