TASK12_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取前5条评论中等级最低用户的被回复评论的点赞数。",
    "properties": {
        "like_count": {
            "type": "integer",
            "description": "该被回复评论的点赞数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["like_count"],
    "additionalProperties": False,
}


def validate_task_12(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    like_count = extracted_answer.get("like_count")
    return like_count == 67
