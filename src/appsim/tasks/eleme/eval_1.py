from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_COUPONS_PAGE = "enter_coupons_page"
PAGE_COUPONS = "coupons"
PAGE_INFO_KEY = "page_info"
PAGE_INFO_TITLE_KEY = "title"
PAGE_INFO_TITLE_VALUE = "红包卡券"
PAGE_INFO_SCREEN_NAME_KEY = "screen_name"
PAGE_INFO_SCREEN_NAME_VALUE = "CouponsScreen"

TASK1_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取红包卡券中红包的总价值。",
    "properties": {
        "total_value": {
            "type": "integer",
            "description": "红包总价值金额，必须是阿拉伯数字整数，不含单位。",
        }
    },
    "required": ["total_value"],
    "additionalProperties": False,
}


def verify_coupon_total_value(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
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

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_value = extracted_answer.get("total_value")
    return total_value == 84
