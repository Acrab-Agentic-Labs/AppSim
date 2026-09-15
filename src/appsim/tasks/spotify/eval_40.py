TASK40_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the title and publish date of the first audiobook.",
    "properties": {
        "audiobook_title": {
            "type": "string",
            "description": "The full title of the first audiobook.",
        },
        "publish_date": {
            "type": "string",
            "description": "The publish date of the first audiobook.",
        }
    },
    "required": ["audiobook_title", "publish_date"],
    "additionalProperties": False,
}


def verify_first_audiobook_title_and_publish_date(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    title = str(extracted_answer.get("audiobook_title") or "").lower()
    date = str(extracted_answer.get("publish_date") or "")
    has_title = "art of reading" in title or ("art" in title and "reading" in title)
    has_date = len(date.strip()) > 0
    return has_title and has_date
