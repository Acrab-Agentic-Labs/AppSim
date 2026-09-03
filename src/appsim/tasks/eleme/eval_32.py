TASK32_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取周账单中吃湘菜花费的金额。",
    "properties": {
        "amount": {
            "type": "string",
            "description": "湘菜花费金额数值。仅输出数字，不含单位和货币符号。",
        }
    },
    "required": ["amount"],
    "additionalProperties": False,
}


def verify_weekly_cuisine_spending_amount(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    amount = str(extracted_answer.get("amount") or "")
    return "102" in amount
