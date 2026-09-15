TASK36_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the lowest average price among all shopping lists.",
    "properties": {
        "lowest_average_price": {
            "type": "string",
            "description": "The lowest average price rounded to two decimal places. Numbers only, no currency symbol.",
        }
    },
    "required": ["lowest_average_price"],
    "additionalProperties": False,
}


def verify_lowest_shopping_list_average_price(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    price = str(extracted_answer.get("lowest_average_price") or "")
    return "29.48" in price
