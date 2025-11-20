import json
import subprocess
import os


def validate_task_twenty(result=None, device_id=None, backup_dir=None):
    """验证任务二十：设置Apple产品京东自营旗舰店的聊天为消息免打扰"""
    mute_settings_file_path = os.path.join(backup_dir, 'mute_settings.json') if backup_dir else 'mute_settings.json'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/mute_settings.json'])
    subprocess.run(cmd, stdout=open(mute_settings_file_path, 'w'))

    try:
        with open(mute_settings_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # mute_settings.json是MuteSetting的数组
            settings = data if isinstance(data, list) else []
    except:
        return False

    # 检查设置中是否包含Apple产品京东自营旗舰店的免打扰设置
    for setting in settings:
        if isinstance(setting, dict):
            # MuteSetting结构: senderName和isMuted
            sender_name = setting.get('senderName', '')
            is_muted = setting.get('isMuted', False)

            if sender_name == 'Apple产品京东自营旗舰店' and is_muted:
                return True

    return False


if __name__ == '__main__':
    result = validate_task_twenty()
    print(result)
