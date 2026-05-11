def validate_task_2(result=None, device_id=None, backup_dir=None):
    """
    任务2: 看一下首页罗翔老师的第一个视频点赞加投币一共多少
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '5.1万' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_2()
    print(result)
