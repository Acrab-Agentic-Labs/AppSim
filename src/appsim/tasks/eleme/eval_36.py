def validate_task_thirty_six(result=None,device_id=None,backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_message中是否包含 "14"
    if 'final_message' in result and (
            "14家" in result['final_message'] or
            "十四家" in result['final_message'] or
            "14个" in result['final_message'] or
            "十四个" in result['final_message'] or
            "14" in result['final_message'] or
            "十四" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_thirty_six()
    print(result)
