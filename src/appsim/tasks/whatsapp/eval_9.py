# Task 9: Check how many communities I have joined.
def validate_task_nine(result=None, device_id=None, backup_dir=None):
    """Verify task 9: answer "3"."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "3" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_nine()
    print(result)
