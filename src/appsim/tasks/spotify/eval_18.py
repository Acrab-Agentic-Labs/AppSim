TASK18_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the first line of lyrics from the song IRIS OUT.",
    "properties": {
        "first_line": {
            "type": "string",
            "description": "The first line of the lyrics.",
        }
    },
    "required": ["first_line"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    line = str(extracted_answer.get("first_line") or "").lower()
    return "i close my eyes and see" in line or (
        "close" in line and "eyes" in line and "see" in line
    )
