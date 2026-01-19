def validate_task_two(result=None,device_id=None,backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_messages中是否包含 "肯德基"
    if 'final_message' in result and '肯德基' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_two()
    print(result)
