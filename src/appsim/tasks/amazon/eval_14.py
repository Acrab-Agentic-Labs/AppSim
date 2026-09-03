TASK14_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total amount of the canceled order.",
    "properties": {
        "total_amount": {
            "type": "string",
            "description": "The total amount as a decimal number. Numbers only, no currency symbol.",
        }
    },
    "required": ["total_amount"],
    "additionalProperties": False,
}


def verify_canceled_order_total_amount(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_amount = str(extracted_answer.get("total_amount") or "")
    return "449.99" in total_amount
