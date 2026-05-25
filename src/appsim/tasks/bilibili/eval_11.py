TASK11_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取接收消息通知总开关的状态。",
    "properties": {
        "status": {
            "type": "string",
            "description": "接收消息通知总开关的状态，仅回答'已开启'或'已关闭'。",
        }
    },
    "required": ["status"],
    "additionalProperties": False,
}


def validate_task_11(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    status = str(extracted_answer.get("status") or "")
    return "已关闭" in status
