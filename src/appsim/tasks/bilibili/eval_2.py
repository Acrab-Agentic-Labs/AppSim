TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取罗翔老师第一个视频的点赞加投币总数。",
    "properties": {
        "total": {
            "type": "string",
            "description": "点赞加投币的总数，保留原始格式（如'5.1万'）。",
        }
    },
    "required": ["total"],
    "additionalProperties": False,
}


def verify_first_video_like_coin_total(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total = str(extracted_answer.get("total") or "")
    return "5.1万" in total
