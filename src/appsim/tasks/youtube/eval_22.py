TASK22_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of mini PC-related shorts among the first four.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of mini PC-related shorts. Must be an Arabic numeral integer.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_short_video_subcategory_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    if not isinstance(count, int):
        return False
    return count == 2
