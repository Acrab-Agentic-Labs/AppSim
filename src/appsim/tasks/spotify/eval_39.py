TASK39_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the initial song count for the Chill Vibes playlist when the agent first checks it, not the final count after completing the task.",
    "properties": {
        "initial_song_count": {
            "type": "integer",
            "description": "The song count in the Chill Vibes playlist when the agent first checks the playlist, not the final count after completing the task. Must be an Arabic numeral integer.",
        },
        "final_song_count": {
            "type": "integer",
            "description": "If the final answer explicitly mentions the final number of songs in the Chill Vibes playlist after adding songs, extract it; otherwise leave it null.",
        }
    },
    "required": ["initial_song_count"],
    "additionalProperties": False,
}


def verify_chill_vibes_initial_song_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("initial_song_count")
    return count == 4
