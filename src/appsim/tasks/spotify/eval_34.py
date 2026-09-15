TASK34_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the title and publish date of the third podcast on the podcasts page.",
    "properties": {
        "podcast_title": {
            "type": "string",
            "description": "The full title of the third podcast.",
        },
        "publish_date": {
            "type": "string",
            "description": "The publish date of the third podcast as displayed.",
        }
    },
    "required": ["podcast_title", "publish_date"],
    "additionalProperties": False,
}


def verify_third_podcast_title_and_publish_date(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    title = str(extracted_answer.get("podcast_title") or "").lower()
    date = str(extracted_answer.get("publish_date") or "").lower()
    has_title = "sound of tomorrow" in title or "sound" in title
    has_date = "dec" in date and "8" in date
    return has_title and has_date
