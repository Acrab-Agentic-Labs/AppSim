TASK3_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取账号的名字和ID。",
    "properties": {
        "account_name": {
            "type": "string",
            "description": "账号名称。",
        },
        "account_id": {
            "type": "string",
            "description": "账号ID，纯数字字符串。",
        },
    },
    "required": ["account_name", "account_id"],
    "additionalProperties": False,
}


def verify_account_name_and_id(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("account_name") or "")
    aid = str(extracted_answer.get("account_id") or "")
    return "高德用户" in name and "284834783" in aid
