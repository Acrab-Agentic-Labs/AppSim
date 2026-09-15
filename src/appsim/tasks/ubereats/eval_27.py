TASK27_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total amount spent on pizza in past purchases, excluding delivery fees.",
    "properties": {
        "total_spent": {
            "type": "string",
            "description": "The total amount spent as a number. Numbers only, no currency symbol.",
        }
    },
    "required": ["total_spent"],
    "additionalProperties": False,
}


def verify_past_pizza_spending(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    spent = str(extracted_answer.get("total_spent") or "")
    return "18.99" in spent
