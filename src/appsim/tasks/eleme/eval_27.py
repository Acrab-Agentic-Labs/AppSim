TASK27_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页推荐前十家店铺中免配送费的店铺数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "免配送费的店铺数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_free_delivery_restaurant_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 2
