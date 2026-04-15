def validate_task_nineteen(result=None, device_id=None, backup_dir=None):
    """Validate task 19: search for 'MacBook' and report how many reviews mention 'Battery life' in the result item."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "1102" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_nineteen()
    print(result)
