TASK20_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of items with a rating higher than 4.8.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of items with rating above 4.8. Must be an Arabic numeral integer.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_high_rated_search_result_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    if not isinstance(count, int):
        return False
    return count == 3
