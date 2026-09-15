TASK7_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract whether there is a nearby McDonald's pickup point.",
    "properties": {
        "answer": {
            "type": "string",
            "description": "Answer yes or no only.",
        }
    },
    "required": ["answer"],
    "additionalProperties": False,
}


def verify_nearby_pickup_location_exists(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    answer = str(extracted_answer.get("answer") or "").lower()
    return "yes" in answer
