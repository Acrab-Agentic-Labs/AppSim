TASK16_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取点赞数最高的评论的用户名称。",
    "properties": {
        "username": {
            "type": "string",
            "description": "点赞数最高评论的用户名称，仅输出名称。",
        }
    },
    "required": ["username"],
    "additionalProperties": False,
}


def validate_task_16(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    username = str(extracted_answer.get("username") or "")
    return "用户1号" in username
