TASK5_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取UP主逍遥散人的粉丝数。",
    "properties": {
        "follower_count": {
            "type": "string",
            "description": "逍遥散人的粉丝数，保留原始格式（如'23.5万'或'234500'）。",
        }
    },
    "required": ["follower_count"],
    "additionalProperties": False,
}


def verify_target_up_followers_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = str(extracted_answer.get("follower_count") or "")
    return "23.5" in count or "234500" in count
