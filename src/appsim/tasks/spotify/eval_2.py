TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the name of the currently playing song.",
    "properties": {
        "song_name": {
            "type": "string",
            "description": "The full name of the currently playing song.",
        }
    },
    "required": ["song_name"],
    "additionalProperties": False,
}


def verify_current_playing_song_name(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("song_name") or "").lower()
    return "iris out" in name
