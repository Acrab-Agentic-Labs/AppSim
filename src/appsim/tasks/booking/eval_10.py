from ._shared import evaluate_task


def verify_search_london_to_hong_kong_next_sunday_without_booking(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=10,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_search_london_to_hong_kong_next_sunday_without_booking())
