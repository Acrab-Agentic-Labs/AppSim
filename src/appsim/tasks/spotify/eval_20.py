TASK20_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the first sentence of the artist introduction for Style's artist.",
    "properties": {
        "first_sentence": {
            "type": "string",
            "description": "The first sentence of the artist's introduction.",
        }
    },
    "required": ["first_sentence"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    sentence = str(extracted_answer.get("first_sentence") or "")
    expected = "Taylor Swift is an American singer-songwriter who has become one of the most influential music artists of the 21st century"
    return expected.lower() in sentence.lower()
