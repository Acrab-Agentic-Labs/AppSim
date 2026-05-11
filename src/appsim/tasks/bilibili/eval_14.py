def validate_task_14(result=None, device_id=None, backup_dir=None):
    """
    任务14: 在收藏页面查看该收藏中共收藏了多少个视频
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and (
            '10' in result['final_message'] or
            '十个' in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_14()
    print(result)
