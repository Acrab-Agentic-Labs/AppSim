TASK29_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页推荐前20个商家中月销量超过4000的店铺数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "月销量超过4000的店铺数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_high_sales_restaurant_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 6
