def validate_task_10(result=None, device_id=None, backup_dir=None):
    """
    任务10: 看第一个视频，不算我点的赞，看看评论区前3条评论所有赞加起来有多少
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '4696' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_10()
    print(result)
