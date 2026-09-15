TASK1_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取私信智能拦截的开启状态。",
    "properties": {
        "status": {
            "type": "string",
            "description": "私信智能拦截的状态，仅回答'已开启'或'未开启'。",
        }
    },
    "required": ["status"],
    "additionalProperties": False,
}


def verify_private_message_intercept_status(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    status = str(extracted_answer.get("status") or "")
    return "未开启" in status and "已开启" not in status
