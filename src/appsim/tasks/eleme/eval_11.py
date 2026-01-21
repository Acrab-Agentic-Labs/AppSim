from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_CHANGE_SETTING = "change_setting"
PAGE_SETTINGS = "settings"
SETTING_TYPE_VALUE = "系统消息通知"

def validate_task_eleven(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    data = None
    for record in reversed(all_data):
        if record.get('action') == ACTION_CHANGE_SETTING:
            extra_data = record.get('extra_data', {})
            if extra_data.get('setting_type') == SETTING_TYPE_VALUE:
                data = record
                break

    if data is None or data.get('page') != PAGE_SETTINGS:
        return False
    if 'timestamp' not in data or not isinstance(data['timestamp'], (int, float)):
        return False

    extra_data = data.get('extra_data', {})
    if extra_data.get('setting_type') != SETTING_TYPE_VALUE or extra_data.get('enabled', True) or not extra_data.get('show_dialog', False):
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_eleven()
    print(result)
