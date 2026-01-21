from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_COUPONS_PAGE = "enter_coupons_page"
PAGE_COUPONS = "coupons"
PAGE_INFO_KEY = "page_info"
PAGE_INFO_TITLE_KEY = "title"
PAGE_INFO_TITLE_VALUE = "红包卡券"
PAGE_INFO_SCREEN_NAME_KEY = "screen_name"
PAGE_INFO_SCREEN_NAME_VALUE = "CouponsScreen"

def validate_task_one(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        # 兼容对象和数组两种格式
        if isinstance(all_data, list):
            data = all_data[-1] if all_data else {}
        else:
            data = all_data
    except:
        return False

    if data.get('action') != ACTION_ENTER_COUPONS_PAGE:
        return False
    if data.get('page') != PAGE_COUPONS:
        return False
    if PAGE_INFO_KEY not in data:
        return False
    page_info = data[PAGE_INFO_KEY]
    if page_info.get(PAGE_INFO_TITLE_KEY) != PAGE_INFO_TITLE_VALUE:
        return False
    if page_info.get(PAGE_INFO_SCREEN_NAME_KEY) != PAGE_INFO_SCREEN_NAME_VALUE:
        return False
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_messages中是否包含 "84"
    if 'final_message' in result and (
            "84元" in result['final_message'] or
            "84块" in result['final_message'] or
            "￥84" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_one()
    print(result)
