TASK20_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the name of the cheapest burger at McDonald's on the home page.",
    "properties": {
        "burger_name": {
            "type": "string",
            "description": "The full name of the cheapest burger.",
        }
    },
    "required": ["burger_name"],
    "additionalProperties": False,
}


def verify_cheapest_homepage_burger(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("burger_name") or "").lower()
    return "mcchicken" in name
