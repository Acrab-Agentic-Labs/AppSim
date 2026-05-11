def validate_task_11(result=None, device_id=None, backup_dir=None):
    """
    任务11: 看一下接收消息通知总开关的状态
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '已关闭' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_11()
    print(result)
