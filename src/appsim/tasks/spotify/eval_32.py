TASK32_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the first line of lyrics and the lyricist of the song Blank Space.",
    "properties": {
        "first_lyric_line": {
            "type": "string",
            "description": "The first line of the lyrics.",
        },
        "lyricist": {
            "type": "string",
            "description": "The name of the lyricist (songwriter).",
        }
    },
    "required": ["first_lyric_line", "lyricist"],
    "additionalProperties": False,
}


def verify_blank_space_first_lyrics_line_and_lyricist(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    line = str(extracted_answer.get("first_lyric_line") or "").lower()
    lyricist = str(extracted_answer.get("lyricist") or "").lower()
    has_lyrics = "close" in line and "eyes" in line
    has_lyricist = "taylor swift" in lyricist
    return has_lyrics and has_lyricist
