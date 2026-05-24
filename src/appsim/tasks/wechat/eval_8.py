TASK8_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取好友发的朋友圈总条数。",
    "properties": {
        "moments_count": {
            "type": "integer",
            "minimum": 0,
            "description": "好友发的朋友圈总条数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["moments_count"],
    "additionalProperties": False,
}


def task8_moments_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("moments_count") == 5:
        return True
    return False
