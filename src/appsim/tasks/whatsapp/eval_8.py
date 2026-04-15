# Task 8: Check how many conversations have unread messages and give me an Arabic numeral only.
def validate_task_eight(result=None, device_id=None, backup_dir=None):
    """Verify task 8: answer "8"."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "8" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_eight()
    print(result)
