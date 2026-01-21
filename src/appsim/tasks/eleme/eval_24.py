from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_NAVIGATE = "navigate"
ACTION_CLEAR_SEARCH_HISTORY = "clear_search_history"
PAGE_SEARCH = "search"

def validate_task_twenty_four(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    if not all_data:
        return False

    entered_search = any(r.get('action') == ACTION_NAVIGATE and r.get('page') == PAGE_SEARCH for r in all_data)
    if not entered_search:
        return False

    clicked_clear_history = any(r.get('action') == ACTION_CLEAR_SEARCH_HISTORY and r.get('page') == PAGE_SEARCH for r in all_data)
    if not clicked_clear_history:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = (
        validate_task_twenty_four())
    print(result)
