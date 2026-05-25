TASK21_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the price difference between the cheapest items at Matchaful and HAWA SMOOTHIES.",
    "properties": {
        "price_difference": {
            "type": "string",
            "description": "The price difference as a number. Numbers only, no currency symbol.",
        }
    },
    "required": ["price_difference"],
    "additionalProperties": False,
}


def validate_task_twenty_one(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    diff = str(extracted_answer.get("price_difference") or "")
    return "1.3" in diff
