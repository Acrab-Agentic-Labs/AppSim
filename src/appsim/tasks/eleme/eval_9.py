import subprocess
import json
import os

def validate_task_nine(result=None,device_id=None,backup_dir=None):
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

    if data.get('action') != 'cart_checkout_success':
        return False
    if data.get('page') != 'cart':
        return False
    if 'extra_data' not in data:
        return False
    extra_data = data['extra_data']
    # 【关键】必须全选
    if not extra_data.get('select_all', False):
        return False
    # 【关键】必须进入结算页面
    if not extra_data.get('entered_checkout', False):
        return False
    # 【关键】必须支付成功
    if not extra_data.get('payment_success', False):
        return False
    return True

if __name__ == '__main__':
    result = validate_task_nine()
    print(result)
