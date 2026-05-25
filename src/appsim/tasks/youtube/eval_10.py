TASK10_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the duration of the first video in liked videos.",
    "properties": {
        "duration": {
            "type": "string",
            "description": "The duration of the video in M:SS format (e.g., '3:58').",
        }
    },
    "required": ["duration"],
    "additionalProperties": False,
}


def validate_task_ten(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    duration = str(extracted_answer.get("duration") or "")
    return "3:58" in duration
