from ._shared import evaluate_task


def verify_submit_five_star_review_for_last_stay(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=4,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_submit_five_star_review_for_last_stay())
