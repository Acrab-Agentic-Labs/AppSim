def validate_task_31(result=None,device_id=None,backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 检测 result 中的final_message中是否包含到期相关信息
    if 'final_message' in result:
        message = result['final_message']
        keywords = ['到期', '天', '月', '年', '日期', '时间', '2024', '2025', '2026']
        if any(keyword in message for keyword in keywords):
            return True

    return False

if __name__ == '__main__':
    result = validate_task_31()
    print(result)
