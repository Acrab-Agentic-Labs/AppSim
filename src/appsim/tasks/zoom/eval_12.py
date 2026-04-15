from ._shared import evaluate_task


def verify_raise_lower_hand_with_thumbs_up(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=12,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_raise_lower_hand_with_thumbs_up())
