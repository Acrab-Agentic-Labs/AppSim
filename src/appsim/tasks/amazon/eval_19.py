TASK19_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of reviews that mention 'Battery life'.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of reviews mentioning 'Battery life'.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_search_result_review_keyword_count(result=None, device_id=None, backup_dir=None):
    """Validate task 19: search for 'MacBook' and report how many reviews mention 'Battery life' in the result item."""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("count") == 1102


if __name__ == "__main__":
    result = verify_search_result_review_keyword_count()
    print(result)
