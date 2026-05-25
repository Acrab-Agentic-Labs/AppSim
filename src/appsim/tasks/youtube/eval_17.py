TASK17_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total number of likes in the comments section.",
    "properties": {
        "total_likes": {
            "type": "integer",
            "description": "The total number of likes across all comments. Must be an Arabic numeral integer.",
        }
    },
    "required": ["total_likes"],
    "additionalProperties": False,
}


def validate_task_seventeen(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_likes = extracted_answer.get("total_likes")
    if not isinstance(total_likes, int):
        return False
    return total_likes == 97
