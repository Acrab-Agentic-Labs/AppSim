TASK10_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取朋友圈点赞人数。",
    "properties": {
        "like_count": {
            "type": "integer",
            "minimum": 0,
            "description": "朋友圈点赞人数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["like_count"],
    "additionalProperties": False,
}


def verify_friend_moments_like_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("like_count") == 14:
        return True
    return False
