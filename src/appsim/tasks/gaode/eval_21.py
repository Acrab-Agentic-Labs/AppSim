TASK21_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取最近的四星级酒店名称。",
    "properties": {
        "hotel_name": {
            "type": "string",
            "description": "四星级酒店的完整名称。",
        }
    },
    "required": ["hotel_name"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("hotel_name") or "")
    return "瑞安城市酒店" in name
