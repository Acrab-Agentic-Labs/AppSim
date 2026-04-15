from ._shared import evaluate_task


def verify_schedule_tomorrow_1900_with_derek_and_brittany(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=15,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_schedule_tomorrow_1900_with_derek_and_brittany())
