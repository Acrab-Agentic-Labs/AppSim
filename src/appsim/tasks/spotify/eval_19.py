TASK19_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the lyricist of the song Style from the credits.",
    "properties": {
        "lyricist": {
            "type": "string",
            "description": "The name of the lyricist (songwriter).",
        }
    },
    "required": ["lyricist"],
    "additionalProperties": False,
}


def verify_style_lyricist(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    lyricist = str(extracted_answer.get("lyricist") or "").lower()
    return "taylor swift" in lyricist
