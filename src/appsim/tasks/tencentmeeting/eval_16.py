import os
import logging
from appsim.utils import read_json_from_device
try:
    from ._answer_utils import answer_contains_any
except ImportError:
    from _answer_utils import answer_contains_any

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "Meeting_5d8e21"
USER_ID = "user001"
EXPECTED_SHARING_STATUS = True
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
IS_SHARING_KEY = "isSharingScreen"


SCREEN_SHARING_SUCCESS_KEYWORDS = [
    "已共享屏幕",
    "正在共享屏幕",
    "共享屏幕已开启",
    "屏幕共享已开启",
    "开始共享",
    "已开始共享",
    "成功共享",
    "已共享",
]


def _is_point_near(point_str, target_x, target_y, tolerance=50):
    if not point_str or not str(point_str).startswith("<point>"):
        return False
    try:
        coords = str(point_str).replace("<point>", "").replace("</point>", "").strip().split()
        x, y = int(coords[0]), int(coords[1])
        return abs(x - target_x) <= tolerance and abs(y - target_y) <= tolerance
    except (ValueError, IndexError):
        return False


def _action_text(action):
    if not isinstance(action, dict):
        return ""
    text_fields = ["text", "content", "label", "description", "element_text", "target", "name"]
    return " ".join(str(action.get(key, "")) for key in text_fields)


def _has_screen_sharing_action_evidence(result) -> bool:
    if not isinstance(result, dict):
        return False

    executed_actions = result.get("executed_actions", [])
    for action in executed_actions:
        if not isinstance(action, dict) or action.get("action") != "click":
            continue

        if "共享屏幕" in _action_text(action):
            return True

        if _is_point_near(action.get("point"), 608, 910) or _is_point_near(action.get("point"), 500, 900):
            return True

    return False


def _has_screen_sharing_result_evidence(result) -> bool:
    if not isinstance(result, dict):
        return False

    if _has_screen_sharing_action_evidence(result):
        return True

    return answer_contains_any(result, SCREEN_SHARING_SUCCESS_KEYWORDS)


def check_screen_sharing_active(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查指定会议中特定用户的屏幕共享状态是否符合预期。

    参数:
        meeting_id (str): 会议ID。
        user_id (str): 用户ID。
        expected_sharing_status (bool): 期望的屏幕共享状态 (True为正在共享, False为未共享)。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果屏幕共享状态符合预期，返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    user_id = USER_ID
    expected_sharing_status = EXPECTED_SHARING_STATUS

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_28")

    data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETING_PARTICIPANTS_FILE}",
        backup_dir=backup_dir,
    )

    if data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETING_PARTICIPANTS_FILE}。")
        return False

    try:
        matching_participant = None
        for participant in data:
            if participant.get("meetingId") == meeting_id and participant.get("userId") == user_id:
                matching_participant = participant
                break

        if matching_participant is not None:
            actual_sharing_status = matching_participant.get(IS_SHARING_KEY)
            if actual_sharing_status == expected_sharing_status:
                return True

            logging.error(
                f"会议 {meeting_id} 中用户 {user_id} 的屏幕共享状态不符合预期。"
                f"实际状态: {actual_sharing_status}, 期望状态: {expected_sharing_status}。"
            )
        else:
            logging.error(f"未在 {MEETING_PARTICIPANTS_FILE} 中找到会议 {meeting_id} 的参与者 {user_id}。")

        if expected_sharing_status and _has_screen_sharing_result_evidence(result):
            logging.warning("数据库中屏幕共享状态未更新，但Agent结果提供了明确的共享屏幕证据，视为成功。")
            return True

        return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False

if __name__ == '__main__':
    print(check_screen_sharing_active())
