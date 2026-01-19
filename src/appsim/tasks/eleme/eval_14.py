from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_ORDERS_PAGE = "enter_orders_page"
ACTION_NAVIGATE_TO_STORE = "navigate_to_store"
ACTION_SHARE_STORE = "share_store"
PAGE_ORDERS = "orders"
PAGE_STORE_PAGE = "store_page"
KEYWORD_MALATANG = "麻辣烫"
PLATFORM_VALUE = "微信"

def validate_task_fourteen(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    found_orders_page = any(r.get('action') == ACTION_ENTER_ORDERS_PAGE and r.get('page') == PAGE_ORDERS for r in all_data)
    if not found_orders_page:
        return False

    found_navigate_to_malatang_store = any(
        r.get('action') == ACTION_NAVIGATE_TO_STORE and
        r.get('page') == PAGE_STORE_PAGE and
        KEYWORD_MALATANG in r.get('page_info', {}).get('restaurant_name', '')
        for r in all_data
    )
    if not found_navigate_to_malatang_store:
        return False

    share_record = next((r for r in reversed(all_data) if r.get('action') == ACTION_SHARE_STORE), None)
    if share_record is None or share_record.get('page') != PAGE_STORE_PAGE:
        return False
    if share_record.get('extra_data', {}).get('platform') != PLATFORM_VALUE:
        return False
    if KEYWORD_MALATANG not in share_record.get('page_info', {}).get('restaurant_name', ''):
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_fourteen()
    print(result)
