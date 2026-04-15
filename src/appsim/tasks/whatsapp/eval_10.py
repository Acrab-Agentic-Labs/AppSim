# Task 10: Check how many statuses the Spotify channel has posted in total and give me an Arabic numeral only.
def validate_task_ten(result=None, device_id=None, backup_dir=None):
    """Verify task 10: answer "10"."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "10" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_ten()
    print(result)
