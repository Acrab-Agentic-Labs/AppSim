TASK11_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total cost of all items currently in the cart.",
    "properties": {
        "total_cost": {
            "type": "string",
            "description": "The total cost as a number. Numbers only, no currency symbol.",
        }
    },
    "required": ["total_cost"],
    "additionalProperties": False,
}


def verify_cart_total_price(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    cost = str(extracted_answer.get("total_cost") or "")
    return "20.19" in cost
