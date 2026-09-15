TASK13_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the count of merchants with free delivery among the first eight on the home page.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of merchants with free delivery. Must be an Arabic numeral integer.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_free_delivery_merchant_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 7
