TASK4_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取购物车中电子产品的总价。",
    "properties": {
        "total_price": {
            "type": "integer",
            "description": "购物车中电子产品的总价，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total_price"],
    "additionalProperties": False,
}


def verify_cart_electronics_total_price(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_price = extracted_answer.get("total_price")
    if total_price is None:
        return False
    return int(total_price) == 21395
