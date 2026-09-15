TASK7_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the name of the first audiobook.",
    "properties": {
        "audiobook_name": {
            "type": "string",
            "description": "The full name of the first audiobook.",
        }
    },
    "required": ["audiobook_name"],
    "additionalProperties": False,
}


def verify_first_audiobook_name(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("audiobook_name") or "").lower()
    return "art of reading" in name or ("art" in name and "reading" in name)
