TASK3_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取会员购前四个商品的总价。",
    "properties": {
        "total_price": {
            "type": "string",
            "description": "前四个商品全部买下来的总价格，保留小数。",
        }
    },
    "required": ["total_price"],
    "additionalProperties": False,
}


def verify_member_purchase_total(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_price = str(extracted_answer.get("total_price") or "")
    return "269.6" in total_price
