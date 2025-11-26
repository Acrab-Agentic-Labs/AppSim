import subprocess
import json
import os

def validate_task_eight(result=None,device_id=None,backup_dir=None):
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

    if data.get('action') != 'change_setting':
        return False
    if data.get('page') != 'settings':
        return False
    if 'extra_data' not in data:
        return False
    extra_data = data['extra_data']
    # 【关键】设置类型必须是"免密支付"
    if extra_data.get('setting_type') != '免密支付':
        return False
    # 【关键】必须开启
    if not extra_data.get('enabled', False):
        return False
    # 【关键】必须显示弹窗
    if not extra_data.get('show_dialog', False):
        return False
    return True

if __name__ == '__main__':
    result = validate_task_eight()
    print(result)
