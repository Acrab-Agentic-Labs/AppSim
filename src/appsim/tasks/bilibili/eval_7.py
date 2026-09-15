TASK7_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取关注动态中前十个动态的点赞数加播放量总和。",
    "properties": {
        "total": {
            "type": "integer",
            "description": "点赞数加播放量的总和，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total"],
    "additionalProperties": False,
}


def verify_follow_feed_like_play_total(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total = extracted_answer.get("total")
    return total == 654335
