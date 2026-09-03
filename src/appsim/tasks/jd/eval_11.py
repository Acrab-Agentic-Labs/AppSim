TASK11_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取收到的京东客服消息总数。",
    "properties": {
        "message_count": {
            "type": "integer",
            "description": "收到的京东客服消息总数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["message_count"],
    "additionalProperties": False,
}


def verify_customer_service_message_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("message_count")
    if count is None:
        return False
    return int(count) == 2
