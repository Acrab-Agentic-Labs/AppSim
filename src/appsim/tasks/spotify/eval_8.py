TASK8_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the duration of the first audiobook.",
    "properties": {
        "duration": {
            "type": "string",
            "description": "The duration of the audiobook as displayed.",
        }
    },
    "required": ["duration"],
    "additionalProperties": False,
}


def verify_first_audiobook_duration(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    duration = str(extracted_answer.get("duration") or "").lower()
    return "5" in duration and "32" in duration
