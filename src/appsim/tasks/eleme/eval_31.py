TASK31_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取十月点外卖的次数。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "十月点外卖的总次数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def validate_task_thirty_one(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 6
