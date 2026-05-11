def validate_task_17(result=None, device_id=None, backup_dir=None):
    """
    任务17: 在设置中，查看当前定时关闭状态
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '不开启' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_17()
    print(result)
