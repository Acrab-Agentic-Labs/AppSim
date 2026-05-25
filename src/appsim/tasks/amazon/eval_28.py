TASK28_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the highest average rating among the four categories.",
    "properties": {
        "highest_average_rating": {
            "type": "string",
            "description": "The highest average rating rounded to two decimal places. Must be an Arabic numeral.",
        }
    },
    "required": ["highest_average_rating"],
    "additionalProperties": False,
}


def validate_task_twenty_eight(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    rating = str(extracted_answer.get("highest_average_rating") or "")
    return "4.83" in rating
