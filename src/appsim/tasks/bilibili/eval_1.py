def validate_task_1(result=None, device_id=None, backup_dir=None):
    """
    任务1: 看一下私信智能拦截的开启状态
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '未开启' not in result['final_message'] and '开启' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_1()
    print(result)
