TASK34_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取指定瑞幸能用的券的数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "可用券的数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def validate_task_thirty_four(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 1
