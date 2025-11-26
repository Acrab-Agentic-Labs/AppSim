import subprocess
import json
import os

def validate_task_five(result=None,device_id=None,backup_dir=None):
    message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.myele', 'cat', 'files/messages.json'])
    subprocess.run(cmd, stdout=open(message_file_path, 'w'))

    try:
        with open(message_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                data = data[-1] if data else {}
    except:
        return False

    if data.get('action') != 'enter_orders_page':
        return False
    if data.get('page') != 'orders':
        return False
    if 'extra_data' not in data:
        return False
    extra_data = data['extra_data']
    # 【关键】必须选择"全部"标签
    if extra_data.get('selected_tab') != '全部':
        return False
    if result is None:
        return False

    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    # 检测 result 中的final_messages中是否包含 "待接单"
    if 'final_message' in result and '待接单' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_five()
    print(result)
