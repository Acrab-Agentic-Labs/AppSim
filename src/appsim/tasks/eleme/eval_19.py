TASK19_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取9月花销金额。",
    "properties": {
        "amount": {
            "type": "string",
            "description": "9月花销金额数值。仅输出数字，不含单位和货币符号。",
        }
    },
    "required": ["amount"],
    "additionalProperties": False,
}


def validate_task_nineteen(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    amount = str(extracted_answer.get("amount") or "")
    return "41.48" in amount
