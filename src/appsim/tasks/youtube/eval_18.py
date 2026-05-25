TASK18_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total duration of videos in Watch later.",
    "properties": {
        "duration": {
            "type": "string",
            "description": "The total duration in MM:SS format (e.g., '17:35').",
        }
    },
    "required": ["duration"],
    "additionalProperties": False,
}


def validate_task_eighteen(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    duration = str(extracted_answer.get("duration") or "")
    return "17:35" in duration
