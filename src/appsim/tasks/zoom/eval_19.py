from ._shared import evaluate_task


def verify_delay_tomorrow_noon_to_1300(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=19,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_delay_tomorrow_noon_to_1300())
