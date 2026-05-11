def validate_task_5(result=None, device_id=None, backup_dir=None):
    """
    任务5: 在关注列表去UP主逍遥散人主页查看其粉丝数
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and (
            '23.5' in result['final_message'] or
            '234500' in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_5()
    print(result)
