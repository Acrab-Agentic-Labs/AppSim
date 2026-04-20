def validate_task_two(result=None, device_id=None, backup_dir=None):
    """Validate task 2: calculate the total price of the items in the cart and return only an Arabic numeral."""

    # Check whether result["final_message"] contains the expected number.
    if result and "final_message" in result and result["final_message"] is not None:
        if "5472.84" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_two()
    print(result)
