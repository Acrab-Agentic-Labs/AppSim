def validate_task_20(result=None, device_id=None, backup_dir=None):
    """
    任务20: 查看大会员是否到期
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '已到期' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_20()
    print(result)
