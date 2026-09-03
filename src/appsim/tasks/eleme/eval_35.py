TASK35_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取账单中九月消费最多的商家名称。",
    "properties": {
        "shop_name": {
            "type": "string",
            "description": "消费最多的商家完整名称，仅输出名称，不含额外描述。",
        }
    },
    "required": ["shop_name"],
    "additionalProperties": False,
}


def verify_highest_spending_restaurant(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("shop_name") or "")
    return "湘味轩" in name
