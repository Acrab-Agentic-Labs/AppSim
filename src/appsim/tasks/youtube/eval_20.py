TASK20_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract Jay Chou's follower count.",
    "properties": {
        "follower_count": {
            "type": "string",
            "description": "The follower count as displayed, preserving original format with unit suffix.",
        }
    },
    "required": ["follower_count"],
    "additionalProperties": False,
}


def verify_channel_follower_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    follower_count = str(extracted_answer.get("follower_count") or "").lower()
    return "3.36m" in follower_count or "3.36 million" in follower_count
