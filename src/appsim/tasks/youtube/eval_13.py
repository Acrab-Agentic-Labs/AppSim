TASK13_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the current App language option.",
    "properties": {
        "language": {
            "type": "string",
            "description": "The current app language setting value.",
        }
    },
    "required": ["language"],
    "additionalProperties": False,
}


def validate_task_thirteen(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    language = str(extracted_answer.get("language") or "")
    return "English(China)" in language or "English (China)" in language
