TASK38_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取粤式早茶所有商品中销量最高的商品名称。",
    "properties": {
        "product_name": {
            "type": "string",
            "description": "销量最高的商品完整名称，仅输出名称，不含额外描述。",
        }
    },
    "required": ["product_name"],
    "additionalProperties": False,
}


def validate_task_thirty_eight(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("product_name") or "")
    return "萝卜糕" in name
