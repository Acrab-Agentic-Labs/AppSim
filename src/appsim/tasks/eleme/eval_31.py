def validate_task_thirty_one(result=None,device_id=None,backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_message中是否包含 "6"
    if 'final_message' in result and (
            "6家" in result['final_message'] or
            "六家" in result['final_message'] or
            "6个" in result['final_message'] or
            "六个" in result['final_message'] or
            "6" in result['final_message'] or
            "六" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_thirty_one()
    print(result)
