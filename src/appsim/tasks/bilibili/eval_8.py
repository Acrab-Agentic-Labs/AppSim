def validate_task_8(result=None, device_id=None, backup_dir=None):
    """
    任务8: 数一下关注列表有几个已互粉的up主
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and (
            '1' in result['final_message'] or
            '一个' in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_8()
    print(result)
