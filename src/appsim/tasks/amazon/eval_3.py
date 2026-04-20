def validate_task_three(result=None, device_id=None, backup_dir=None):
    """Validate task 3: check how many 'Lifestyle' items are in the Interests section and return only an Arabic numeral."""

    # Check whether result["final_message"] contains the expected number.
    if result and "final_message" in result and result["final_message"] is not None:
        if "4" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_three()
    print(result)
