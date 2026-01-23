from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_FOOD_INSURANCE_PAGE = "enter_food_insurance_page"
ACTION_APPLY_FOOD_INSURANCE = "apply_food_insurance"
PAGE_FOOD_INSURANCE = "food_insurance"
KEYWORD_MALATANG = "麻辣烫"

def validate_task_twenty_one(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    if not all_data:
        return False

    entered_insurance = any(
        r.get('action') == ACTION_ENTER_FOOD_INSURANCE_PAGE and
        r.get('page') == PAGE_FOOD_INSURANCE and
        KEYWORD_MALATANG in r.get('extra_data', {}).get('restaurant_name', '')
        for r in all_data
    )
    if not entered_insurance:
        return False

    applied_insurance = any(
        r.get('action') == ACTION_APPLY_FOOD_INSURANCE and
        r.get('page') == PAGE_FOOD_INSURANCE and
        r.get('extra_data', {}).get('apply_successfully') == True
        for r in all_data
    )
    if not applied_insurance:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_twenty_one()
    print(result)
