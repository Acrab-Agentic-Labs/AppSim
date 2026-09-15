TASK24_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract whether the user prefers Burger or Pizza based on past purchases.",
    "properties": {
        "preference": {
            "type": "string",
            "description": "The food preference: either 'Burger' or 'Pizza'.",
        }
    },
    "required": ["preference"],
    "additionalProperties": False,
}


def verify_preferred_food_category(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    pref = str(extracted_answer.get("preference") or "").lower()
    return "burger" in pref
