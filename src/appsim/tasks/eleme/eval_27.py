def validate_task_twenty_seven(result=None,device_id=None,backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and (
            "2家" in result['final_message'] or
            "二家" in result['final_message'] or
            "两家" in result['final_message'] or
            "2个" in result['final_message'] or
            "二个" in result['final_message'] or
            "两个" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_twenty_seven()
    print(result)

