def validate_task_18(result=None, device_id=None, backup_dir=None):
    """
    任务18: 在直播推荐页面，查看前四个推荐直播中人数最少的两个的在线观看人数一共多少
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '8623' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_18()
    print(result)
