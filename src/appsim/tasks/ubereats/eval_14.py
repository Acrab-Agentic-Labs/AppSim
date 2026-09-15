TASK14_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the remaining balance in the Uber account.",
    "properties": {
        "balance": {
            "type": "string",
            "description": "The account balance as a number. Numbers only, no currency symbol.",
        }
    },
    "required": ["balance"],
    "additionalProperties": False,
}


def verify_account_balance(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    balance = str(extracted_answer.get("balance") or "")
    return "0" in balance
