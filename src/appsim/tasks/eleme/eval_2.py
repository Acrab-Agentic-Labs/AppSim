TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取好评最高的10家店中月销量最高的店铺名称。",
    "properties": {
        "shop_name": {
            "type": "string",
            "description": "月销量最高的店铺完整名称，仅输出名称，不含额外描述。",
        }
    },
    "required": ["shop_name"],
    "additionalProperties": False,
}


def verify_highest_sales_among_top_rated_restaurants(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("shop_name") or "")
    return "肯德基" in name
