from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_CHANGE_PHONE_PAGE = "enter_change_phone_page"
PAGE_CHANGE_PHONE = "change_phone"

def verify_phone_edit_page_opened(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        data = all_data[-1] if isinstance(all_data, list) and all_data else all_data
    except:
        return False

    if data.get('action') != ACTION_ENTER_CHANGE_PHONE_PAGE or data.get('page') != PAGE_CHANGE_PHONE:
        return False
    return True

if __name__ == '__main__':
    result = verify_phone_edit_page_opened()
    print(result)