def validate_task_thirty_four(result=None,device_id=None,backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_message中是否包含 "1"
    if 'final_message' in result and (
            "1张" in result['final_message'] or
            "一张" in result['final_message'] or
            "1个" in result['final_message'] or
            "一个" in result['final_message'] or
            "1" in result['final_message'] or
            "一" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_thirty_four()
    print(result)
