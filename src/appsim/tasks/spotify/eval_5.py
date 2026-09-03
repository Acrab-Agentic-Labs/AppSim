TASK5_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the title of the first podcast on the podcasts page.",
    "properties": {
        "podcast_title": {
            "type": "string",
            "description": "The full title of the first podcast.",
        }
    },
    "required": ["podcast_title"],
    "additionalProperties": False,
}


def verify_first_podcast_title(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    title = str(extracted_answer.get("podcast_title") or "").lower()
    return "how ai is changing music" in title or ("ai" in title and "music" in title)
