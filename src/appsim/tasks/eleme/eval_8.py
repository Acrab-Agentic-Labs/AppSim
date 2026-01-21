from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_CHANGE_SETTING = "change_setting"
PAGE_SETTINGS = "settings"
SETTING_TYPE_VALUE = "免密支付"

def validate_task_eight(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        data = all_data[-1] if isinstance(all_data, list) and all_data else all_data
    except:
        return False

    if data.get('action') != ACTION_CHANGE_SETTING or data.get('page') != PAGE_SETTINGS:
        return False
    extra_data = data.get('extra_data', {})
    if extra_data.get('setting_type') != SETTING_TYPE_VALUE or not extra_data.get('enabled', False) or not extra_data.get('show_dialog', False):
        return False
    return True

if __name__ == '__main__':
    result = validate_task_eight()
    print(result)
