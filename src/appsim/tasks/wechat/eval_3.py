TASK3_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取参会的听众人数。",
    "properties": {
        "attendee_count": {
            "type": "integer",
            "minimum": 0,
            "description": "参会的听众人数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["attendee_count"],
    "additionalProperties": False,
}


def task3_validate_attendee_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("attendee_count") == 10:
        return True
    return False
