TASK24_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取驾车所需的时间。",
    "properties": {
        "driving_minutes": {
            "type": "integer",
            "minimum": 0,
            "description": "驾车所需分钟数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["driving_minutes"],
    "additionalProperties": False,
}


def verify_driving_duration_to_destination(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("driving_minutes") == 8
