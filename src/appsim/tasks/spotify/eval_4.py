TASK4_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of songs in the first recommended playlist.",
    "properties": {
        "song_count": {
            "type": "integer",
            "description": "The number of songs in the playlist. Must be an Arabic numeral integer.",
        }
    },
    "required": ["song_count"],
    "additionalProperties": False,
}


def verify_first_recommended_playlist_song_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("song_count")
    return isinstance(count, int) and count > 0
