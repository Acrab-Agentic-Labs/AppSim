def validate_task_thirty_six(result=None, device_id=None, backup_dir=None):
    """Validate task 36: calculate the average price of items in each shopping list and report the lowest average price rounded to two decimal places."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "29.48" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_thirty_six()
    print(result)
