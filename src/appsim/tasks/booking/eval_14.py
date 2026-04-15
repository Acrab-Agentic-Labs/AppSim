from ._shared import evaluate_task


def verify_book_cheapest_comfort_sedan_at_hkg(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=14,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_book_cheapest_comfort_sedan_at_hkg())
