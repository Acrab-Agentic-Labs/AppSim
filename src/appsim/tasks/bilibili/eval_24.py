import re

def validate_task_24(result=None,device_id=None,backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 检测 result 中的final_messages中是否包含数字"13"（作为独立的数字）
    if 'final_message' in result:
        # 匹配独立的数字13，可以是"13个"、"13 个"、"共13个"等形式
        pattern = r'\b13\b'
        if re.search(pattern, result['final_message']):
            return True

    return False

if __name__ == '__main__':
    result = validate_task_24()
    print(result)
