TASK6_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the publish date of the first podcast.",
    "properties": {
        "publish_date": {
            "type": "string",
            "description": "The publish date of the first podcast as displayed.",
        }
    },
    "required": ["publish_date"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    date = str(extracted_answer.get("publish_date") or "").lower()
    return "dec" in date and "15" in date
