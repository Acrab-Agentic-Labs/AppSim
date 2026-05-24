TASK15_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取收藏的第一行饭店名称。",
    "properties": {
        "restaurant_name": {
            "type": "string",
            "description": "收藏的第一行饭店的完整名称。",
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
    return "肖记公安牛肉鱼杂馆" in name
