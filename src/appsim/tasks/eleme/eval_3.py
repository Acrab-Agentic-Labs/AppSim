TASK3_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取瑞幸咖啡招牌系列中价格最低的饮品名称。",
    "properties": {
        "drink_name": {
            "type": "string",
            "description": "价格最低的饮品完整名称，仅输出名称，不含价格等额外信息。",
        }
    },
    "required": ["drink_name"],
    "additionalProperties": False,
}


def validate_task_three(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("drink_name") or "")
    return "冷萃咖啡" in name
