# Task 3: Check the phone number linked to my account and tell me the answer only.
def validate_task_three(result=None, device_id=None, backup_dir=None):
    """Verify task 3: answer "+1 (415) 555-0192" or "(415) 555-0192"."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "+1 (415) 555-0192" in result["final_message"] or "(415) 555-0192" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_three()
    print(result)
