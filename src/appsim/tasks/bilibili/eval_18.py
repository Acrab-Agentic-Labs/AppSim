TASK18_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取前四个推荐直播中人数最少的两个的在线观看人数总和。",
    "properties": {
        "total_viewers": {
            "type": "integer",
            "description": "人数最少的两个直播的在线观看人数总和，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total_viewers"],
    "additionalProperties": False,
}


def validate_task_18(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_viewers = extracted_answer.get("total_viewers")
    return total_viewers == 8623
