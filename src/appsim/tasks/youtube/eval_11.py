def validate_task_eleven(result=None,device_id=None,backup_dir=None):
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    if 'final_message' in result and (
            'off' in result['final_message'].lower()
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    print(validate_task_eleven())
