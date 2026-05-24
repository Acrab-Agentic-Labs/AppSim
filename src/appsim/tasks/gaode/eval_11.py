TASK11_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取步行去最近酒店所需的时间。",
    "properties": {
        "walking_minutes": {
            "type": "integer",
            "minimum": 0,
            "description": "步行所需分钟数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["walking_minutes"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("walking_minutes") == 8
