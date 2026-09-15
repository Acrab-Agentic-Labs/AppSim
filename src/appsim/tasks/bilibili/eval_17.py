TASK17_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取设置中当前定时关闭的状态。",
    "properties": {
        "status": {
            "type": "string",
            "description": "定时关闭的当前状态，如'不开启'、'已开启'等。",
        }
    },
    "required": ["status"],
    "additionalProperties": False,
}


def verify_timer_shutdown_status(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    status = str(extracted_answer.get("status") or "")
    return "不开启" in status
