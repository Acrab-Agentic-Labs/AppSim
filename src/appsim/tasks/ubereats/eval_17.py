TASK17_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total amount spent at burger or pizza places from 3.17 to 3.22.",
    "properties": {
        "total_spent": {
            "type": "string",
            "description": "The total amount spent as a number. Numbers only, no currency symbol.",
        }
    },
    "required": ["total_spent"],
    "additionalProperties": False,
}


def verify_category_delivery_spending_between_dates(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    spent = str(extracted_answer.get("total_spent") or "")
    return "116.24" in spent
