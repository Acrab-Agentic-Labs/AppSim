from ._shared import evaluate_task

TASK23_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total amount spent so far.",
    "properties": {
        "amount": {
            "type": "number",
            "description": "The total amount spent, as a numeric value.",
        }
    },
    "required": ["amount"],
    "additionalProperties": False,
}


def verify_total_spending_amount(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=24,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_total_spending_amount())
