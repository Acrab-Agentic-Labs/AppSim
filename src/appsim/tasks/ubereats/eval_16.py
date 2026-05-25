TASK16_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the expected arrival time of the latest order.",
    "properties": {
        "arrival_time": {
            "type": "string",
            "description": "The expected arrival time in H:MM or HH:MM format.",
        }
    },
    "required": ["arrival_time"],
    "additionalProperties": False,
}


def validate_task_sixteen(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    time = str(extracted_answer.get("arrival_time") or "")
    return "9:45" in time or "21:45" in time
