def validate_task_30(result=None, device_id=None, backup_dir=None):
    """
    任务30: 搜索原神，观看搜索到的第一个视频，看一下点赞最高的那个评论说的什么
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '能不能出一期队伍配置推荐' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_30()
    print(result)
