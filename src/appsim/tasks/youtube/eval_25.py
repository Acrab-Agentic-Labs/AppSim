TASK25_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of likes on the newest comment.",
    "properties": {
        "likes": {
            "type": "integer",
            "description": "The number of likes on the newest comment. Must be an Arabic numeral integer.",
        }
    },
    "required": ["likes"],
    "additionalProperties": False,
}


def validate_task_twenty_five(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    likes = extracted_answer.get("likes")
    if not isinstance(likes, int):
        return False
    return likes == 8
