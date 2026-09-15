TASK33_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取粉丝量更高的店铺名称。",
    "properties": {
        "store_name": {
            "type": "string",
            "description": "粉丝量更高的店铺完整名称，仅输出名称，不含额外描述。",
        }
    },
    "required": ["store_name"],
    "additionalProperties": False,
}


def verify_higher_follower_store_identified(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("store_name") or "")
    return "Apple官方旗舰店" in name
