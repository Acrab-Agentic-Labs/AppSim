def validate_task_7(result=None, device_id=None, backup_dir=None):
    """
    任务7: 查看关注动态中所有动态的点赞数加播放量一共多少
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '654335' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_7()
    print(result)
