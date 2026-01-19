from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_ORDERS_PAGE = "enter_orders_page"
PAGE_ORDERS = "orders"
EXTRA_DATA_KEY = "extra_data"
EXTRA_DATA_SELECTED_TAB_KEY = "selected_tab"
EXTRA_DATA_SELECTED_TAB_VALUE = "全部"

def validate_task_five(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        if isinstance(all_data, list):
            data = all_data[-1] if all_data else {}
        else:
            data = all_data
    except:
        return False

    if data.get('action') != ACTION_ENTER_ORDERS_PAGE:
        return False
    if data.get('page') != PAGE_ORDERS:
        return False
    if EXTRA_DATA_KEY not in data:
        return False
    extra_data = data[EXTRA_DATA_KEY]
    # 【关键】必须选择"全部"标签
    if extra_data.get(EXTRA_DATA_SELECTED_TAB_KEY) != EXTRA_DATA_SELECTED_TAB_VALUE:
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
