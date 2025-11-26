import subprocess
import json
import os

def validate_task_one(result=None,device_id=None,backup_dir=None):
    message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.myele', 'cat', 'files/messages.json'])
    subprocess.run(cmd, stdout=open(message_file_path, 'w'))

    try:
        with open(message_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 兼容对象和数组两种格式
            if isinstance(data, list):
                data = data[-1] if data else {}
    except:
        return False

    if data.get('action') != 'enter_coupons_page':
        return False
    if data.get('page') != 'coupons':
        return False
    if 'page_info' not in data:
        return False
    page_info = data['page_info']
    if page_info.get('title') != '红包卡券':
        return False
    if page_info.get('screen_name') != 'CouponsScreen':
        return False
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_messages中是否包含 "84"
    if 'final_message' in result and (
            "84元" in result['final_message'] or
            "84块" in result['final_message'] or
            "￥84" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_one()
    print(result)
