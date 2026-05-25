TASK29_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total amount spent on matcha items in past purchases.",
    "properties": {
        "total_spent": {
            "type": "string",
            "description": "The total amount spent as a number. Numbers only, no currency symbol.",
        }
    },
    "required": ["total_spent"],
    "additionalProperties": False,
}


def validate_task_twenty_nine(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    spent = str(extracted_answer.get("total_spent") or "")
    return "14" in spent
