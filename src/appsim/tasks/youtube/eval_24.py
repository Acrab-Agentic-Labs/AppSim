TASK24_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total duration in seconds of computer-related shorts among the first four.",
    "properties": {
        "total_seconds": {
            "type": "integer",
            "description": "The total duration in seconds. Must be an Arabic numeral integer.",
        }
    },
    "required": ["total_seconds"],
    "additionalProperties": False,
}


def validate_task_twenty_four(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_seconds = extracted_answer.get("total_seconds")
    if not isinstance(total_seconds, int):
        return False
    return total_seconds == 139
