TASK12_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取开放时间的小时数。",
    "properties": {
        "open_hours": {
            "type": "integer",
            "minimum": 0,
            "description": "开放时间的小时数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["open_hours"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("open_hours") == 8
