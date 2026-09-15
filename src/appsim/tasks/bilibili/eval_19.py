TASK19_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取会员购前四个商品的购买人数总和。",
    "properties": {
        "total_buyers": {
            "type": "integer",
            "description": "前四个商品的购买人数总和，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total_buyers"],
    "additionalProperties": False,
}


def verify_favorite_items_purchase_total(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_buyers = extracted_answer.get("total_buyers")
    return total_buyers == 4963
