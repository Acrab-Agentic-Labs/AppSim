TASK7_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取已点赞的朋友圈条数。",
    "properties": {
        "liked_count": {
            "type": "integer",
            "minimum": 0,
            "description": "已点赞的朋友圈条数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["liked_count"],
    "additionalProperties": False,
}


def task7_stared_moments_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("liked_count") == 4:
        return True
    return False
