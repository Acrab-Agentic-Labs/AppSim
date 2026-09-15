TASK23_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total likes of computer-related shorts among the first four.",
    "properties": {
        "total_likes": {
            "type": "string",
            "description": "The total number of likes, preserving original format.",
        }
    },
    "required": ["total_likes"],
    "additionalProperties": False,
}


def verify_short_video_category_likes_total(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_likes = str(extracted_answer.get("total_likes") or "")
    return "3.6K" in total_likes or "3.6k" in total_likes or "3600" in total_likes
