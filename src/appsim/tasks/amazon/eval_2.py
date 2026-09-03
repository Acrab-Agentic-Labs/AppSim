TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total price of items in the cart.",
    "properties": {
        "total_price": {
            "type": "string",
            "description": "The total price as a decimal number. Numbers only, no currency symbol.",
        }
    },
    "required": ["total_price"],
    "additionalProperties": False,
}


def verify_cart_total_price(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_price = str(extracted_answer.get("total_price") or "")
    return "5472.84" in total_price
