def validate_task_12(result=None, device_id=None, backup_dir=None):
    """
    任务12: 在首页推荐第一个视频评论页面，查看前5条评论等级最低的那个人的被回复评论的点赞数
    """
    # 验证 result 存在
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_messages中是否包含 "67"
    if 'final_message' in result and '67' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_12()
    print(result)
