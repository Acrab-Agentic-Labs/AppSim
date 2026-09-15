TASK1_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取美食排行榜中评分最高的美食名称。",
    "properties": {
        "restaurant_name": {
            "type": "string",
            "description": "评分最高的美食店铺完整名称。",
        }
    },
    "required": ["restaurant_name"],
    "additionalProperties": False,
}


def verify_top_rated_nearby_food_name(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("restaurant_name") or "")
    return "肖记公安牛肉鱼杂馆" in name
