TASK9_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the artist name of the currently playing song.",
    "properties": {
        "artist_name": {
            "type": "string",
            "description": "The full name of the artist.",
        }
    },
    "required": ["artist_name"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("artist_name") or "").strip()
    return len(name) > 0
