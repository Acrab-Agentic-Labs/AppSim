TASK33_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取能用的最大红包金额。",
    "properties": {
        "amount": {
            "type": "string",
            "description": "最大红包金额数值。仅输出数字，不含单位和货币符号。",
        }
    },
    "required": ["amount"],
    "additionalProperties": False,
}


def validate_task_thirty_three(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    amount = str(extracted_answer.get("amount") or "")
    return "30" in amount
