TASK20_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取大会员是否到期的状态。",
    "properties": {
        "status": {
            "type": "string",
            "description": "大会员状态，仅回答'已到期'或'未到期'。",
        }
    },
    "required": ["status"],
    "additionalProperties": False,
}


def verify_vip_expiration_status(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    status = str(extracted_answer.get("status") or "")
    return "已到期" in status
