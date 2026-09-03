TASK10_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the name of the cheapest item at a nearby McDonald's.",
    "properties": {
        "item_name": {
            "type": "string",
            "description": "The full name of the cheapest menu item.",
        }
    },
    "required": ["item_name"],
    "additionalProperties": False,
}


def verify_cheapest_nearby_menu_item(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("item_name") or "").lower()
    return "hash browns" in name
