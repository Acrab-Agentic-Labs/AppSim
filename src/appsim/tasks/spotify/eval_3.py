TASK3_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total number of categories on the search page.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The total number of categories. Must be an Arabic numeral integer.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_search_page_category_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 14
