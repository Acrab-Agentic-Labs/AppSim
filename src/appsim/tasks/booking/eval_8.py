from ._shared import evaluate_task


def verify_book_hkg_to_lhr_first_class_without_extra_baggage(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=8,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_book_hkg_to_lhr_first_class_without_extra_baggage())
