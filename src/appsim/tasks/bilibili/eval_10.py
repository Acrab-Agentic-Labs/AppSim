TASK10_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取评论区前3条评论所有赞的总数（不含自己点的赞）。",
    "properties": {
        "total_likes": {
            "type": "integer",
            "description": "前3条评论点赞数的总和，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total_likes"],
    "additionalProperties": False,
}


def verify_first_video_comment_like_total(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_likes = extracted_answer.get("total_likes")
    return total_likes == 4696
