TASK37_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页推荐店铺前23家中距离最近的店铺名称。",
    "properties": {
        "shop_name": {
            "type": "string",
            "description": "距离最近的店铺完整名称，仅输出名称，不含额外描述。",
        }
    },
    "required": ["shop_name"],
    "additionalProperties": False,
}


def verify_nearest_recommended_restaurant_name(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("shop_name") or "")
    return "蜜雪冰城" in name
