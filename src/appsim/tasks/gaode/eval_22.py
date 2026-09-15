TASK22_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取停车收费标准。",
    "properties": {
        "hourly_fee": {
            "type": "integer",
            "minimum": 0,
            "description": "每小时停车费用（元），必须是阿拉伯数字整数。",
        }
    },
    "required": ["hourly_fee"],
    "additionalProperties": False,
}


def verify_parking_hourly_fee(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("hourly_fee") == 4
