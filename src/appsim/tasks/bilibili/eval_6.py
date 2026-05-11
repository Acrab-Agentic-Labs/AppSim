def validate_task_6(result=None, device_id=None, backup_dir=None):
    """
    任务6: 进入首页第一个视频，算一下收藏加转发数量一共多少，不算上我的收藏。
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '3999' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_6()
    print(result)
