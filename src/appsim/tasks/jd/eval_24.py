import json
import re

def validate_task_twenty_four(result=None, device_id=None, backup_dir=None):
    """ 验证任务：查看我的订单中，待使用的电子产品共有多少件。"""
    if result and 'final_message' in result:
        message = result['final_message']
        patterns = ['6个', '6件', '6份', '6项', '六个', '六件', '六份', '六项']
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == '__main__':
    result = validate_task_twenty_four()
    print(result)
