def validate_task_twenty_eight(result=None, device_id=None, backup_dir=None):
    """Validate task 28: on the Interests page, check each of the four categories, calculate the average rating of all products in each category, and report the highest average rating rounded to two decimal places."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "4.83" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_twenty_eight()
    print(result)
