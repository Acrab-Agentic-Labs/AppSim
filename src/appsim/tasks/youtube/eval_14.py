TASK14_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of videos about phones in the Apple section.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of phone-related videos. Must be an Arabic numeral integer.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_homepage_section_category_video_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    if not isinstance(count, int):
        return False
    return count == 2
