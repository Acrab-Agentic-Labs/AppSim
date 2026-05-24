TASK14_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取美食排行榜第一的地点的电话号码。",
    "properties": {
        "phone_number": {
            "type": "string",
            "description": "电话号码，保留区号和连接符，格式如 0XX-XXXXXXXX。",
        }
    },
    "required": ["phone_number"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    phone = str(extracted_answer.get("phone_number") or "")
    return "027-83456789" in phone
