TASK22_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total price of the three most expensive items by unit price in the cart.",
    "properties": {
        "total_price": {
            "type": "string",
            "description": "The total price as a decimal number. Numbers only, no currency symbol.",
        }
    },
    "required": ["total_price"],
    "additionalProperties": False,
}


def verify_three_most_expensive_cart_items_total(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_price = str(extracted_answer.get("total_price") or "")
    return "3118.98" in total_price
