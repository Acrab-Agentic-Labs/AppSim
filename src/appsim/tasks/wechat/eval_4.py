TASK4_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取当前微信好友总数。",
    "properties": {
        "friend_count": {
            "type": "integer",
            "minimum": 0,
            "description": "当前微信好友总数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["friend_count"],
    "additionalProperties": False,
}


def task4_validate_friend_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("friend_count") == 101:
        return True
    return False
