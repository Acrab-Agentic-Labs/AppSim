TASK40_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取主页推荐店铺前20家中送达最快的饮品店名称。",
    "properties": {
        "shop_name": {
            "type": "string",
            "description": "送达最快的饮品店完整名称，仅输出名称，不含额外描述。",
        }
    },
    "required": ["shop_name"],
    "additionalProperties": False,
}


def verify_fastest_drink_restaurant_delivery(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("shop_name") or "")
    return "蜜雪冰城" in name
