def validate_task_13(result=None, device_id=None, backup_dir=None):
    """
    任务13: 查看收藏的第一个视频的视频时长
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '03:45' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_13()
    print(result)
