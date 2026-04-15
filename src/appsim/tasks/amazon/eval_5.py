def validate_task_five(result=None, device_id=None, backup_dir=None):
    """Validate task 5: view my order list, calculate how many orders I have in total, and return only an Arabic numeral."""

    # Check whether result["final_message"] contains the expected number.
    if result and "final_message" in result and result["final_message"] is not None:
        if "12" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_five()
    print(result)
