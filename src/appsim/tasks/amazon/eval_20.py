def validate_task_twenty(result=None, device_id=None, backup_dir=None):
    """Validate task 20: search for 'electronics' and count how many items have a rating higher than 4.8."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "3" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_twenty()
    print(result)
