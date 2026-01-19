from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_REVIEWS_PAGE = "enter_reviews_page"
ACTION_SWITCH_TO_REVIEWED = "switch_to_reviewed"
ACTION_DELETE_REVIEW = "delete_review"
PAGE_REVIEWS = "reviews"
SELECTED_TAB_REVIEWED = "已评价"

def validate_task_twenty(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    if not all_data:
        return False

    entered_reviews = any(r.get('action') == ACTION_ENTER_REVIEWS_PAGE and r.get('page') == PAGE_REVIEWS for r in all_data)
    if not entered_reviews:
        return False

    switched_to_reviewed = any(
        r.get('action') == ACTION_SWITCH_TO_REVIEWED and
        r.get('page') == PAGE_REVIEWS and
        r.get('extra_data', {}).get('selected_tab') == SELECTED_TAB_REVIEWED
        for r in all_data
    )
    if not switched_to_reviewed:
        return False

    deleted_review = any(
        r.get('action') == ACTION_DELETE_REVIEW and
        r.get('page') == PAGE_REVIEWS and
        r.get('extra_data', {}).get('deleted_successfully') == True
        for r in all_data
    )
    if not deleted_review:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_twenty()
    print(result)
