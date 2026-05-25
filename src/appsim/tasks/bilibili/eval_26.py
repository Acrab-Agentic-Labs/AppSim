TASK26_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取前20条评论中点赞数最低的用户编号。",
    "properties": {
        "user_number": {
            "type": "integer",
            "description": "点赞数最低的用户编号，必须是阿拉伯数字整数。",
        }
    },
    "required": ["user_number"],
    "additionalProperties": False,
}


def validate_task_26(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    user_number = extracted_answer.get("user_number")
    return user_number == 26
