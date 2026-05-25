TASK8_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取关注列表中已互粉的UP主数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "已互粉的UP主数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def validate_task_8(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 1
