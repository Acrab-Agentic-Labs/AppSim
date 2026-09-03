TASK15_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the count of previously ordered merchants that sell burgers or pizza.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of merchants selling burgers or pizza. Must be an Arabic numeral integer.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_past_category_merchant_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 5
