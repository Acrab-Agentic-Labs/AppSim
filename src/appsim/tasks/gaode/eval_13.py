TASK13_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取M+购物中心的地址。",
    "properties": {
        "address": {
            "type": "string",
            "description": "M+购物中心的完整地址，必须包含省、市、区和街道门牌号，格式如：XX省XX市XX区XX路XXX号。",
        }
    },
    "required": ["address"],
    "additionalProperties": False,
}


def verify_poi_address(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    addr = str(extracted_answer.get("address") or "")
    return "湖北省武汉市江汉区江汉路187号" in addr
