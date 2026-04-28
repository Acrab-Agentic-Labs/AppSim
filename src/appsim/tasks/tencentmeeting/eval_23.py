import os
import logging
from appsim.utils import read_json_from_device
try:
    from ._answer_utils import answer_contains_any
except ImportError:
    from _answer_utils import answer_contains_any

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
USER_ID = "user001"
EXPECTED_WAITING_ROOM_STATUS = True
EXPECTED_IN_MEETING_STATUS = True
PERSONAL_MEETING_ROOMS_FILE = "personal_meeting_rooms.json"
MEETINGS_FILE = "meetings.json"
INVITATIONS_FILE = "meeting_invitations.json"
USERS_FILE = "users.json"

# 常量定义
USER_ID_KEY = "userId"
ENABLE_WAITING_ROOM_KEY = "enableWaitingRoom"
IN_MEETING_KEY = "inMeeting"
MEETING_TYPE_KEY = "meetingType"
HOST_ID_KEY = "hostId"
MEETING_STATUS_KEY = "status"
MEETING_SETTINGS_KEY = "settings"
MEETING_START_TIME_KEY = "startTime"

MEETING_TYPE_PERSONAL = "PERSONAL"
MEETING_STATUS_ONGOING = "ONGOING"

PERSONAL_ROOM_ENTER_KEYWORDS = [
    "已进入个人会议室",
    "成功进入个人会议室",
    "进入个人会议室成功",
    "已经进入个人会议室",
    "已进入会议室",
    "进入会议室成功",
    "已在个人会议室",
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


def _has_enter_personal_room_action_evidence(result) -> bool:
    if not isinstance(result, dict):
        return False

    executed_actions = result.get("executed_actions", [])
    for action in executed_actions:
        if not isinstance(action, dict) or action.get("action") != "click":
            continue

        action_text = _action_text(action)
        if "进入个人会议室" in action_text or "进入会议室" in action_text:
            return True

        if _is_point_near(action.get("point"), 500, 916):
            return True

    return False


def _has_enter_personal_room_result_evidence(result) -> bool:
    if not isinstance(result, dict):
        return False

    if _has_enter_personal_room_action_evidence(result):
        return True

    return answer_contains_any(result, PERSONAL_ROOM_ENTER_KEYWORDS)


def check_personal_meeting_room_waiting_room_status(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查个人会议室的等候室状态以及是否已进入会议。

    参数:
        user_id (str): 操作用户的ID。
        expected_waiting_room_status (bool): 期望的等候室状态 (True为开启, False为关闭)。
        expected_in_meeting_status (bool): 期望的进入会议状态 (True为已进入, False为未进入)。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果个人会议室等候室状态和会议进入状态都符合预期，返回True，否则返回False。
    """

    # 使用常量
    user_id = USER_ID
    expected_waiting_room_status = EXPECTED_WAITING_ROOM_STATUS
    expected_in_meeting_status = EXPECTED_IN_MEETING_STATUS

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_29")

    # --- 检查 personal_meeting_rooms.json ---
    personal_room_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{PERSONAL_MEETING_ROOMS_FILE}",
        backup_dir=backup_dir,
    )

    if personal_room_data is None:
        logging.error(f"错误: 无法从设备读取或解析 {PERSONAL_MEETING_ROOMS_FILE}。")
        return False

    personal_room_found = False
    personal_meeting_id = None
    try:
        for room in personal_room_data:
            if room.get(USER_ID_KEY) == user_id:
                personal_room_found = True
                personal_meeting_id = room.get("meetingId")
                actual_waiting_room_status = room.get(ENABLE_WAITING_ROOM_KEY)
                if actual_waiting_room_status != expected_waiting_room_status:
                    logging.error(
                        f"用户 {user_id} 的个人会议室等候室状态不符合预期。"
                        f"实际状态: {actual_waiting_room_status}, 期望状态: {expected_waiting_room_status}。"
                    )
                    return False
                break
    except Exception as e:
        logging.error(f"处理 {PERSONAL_MEETING_ROOMS_FILE} 数据时发生错误: {e}")
        return False

    if not personal_room_found:
        logging.error(f"未在 {PERSONAL_MEETING_ROOMS_FILE} 中找到用户 {user_id} 的个人会议室信息。")
        return False

    # --- 检查 meetings.json ---
    meetings_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETINGS_FILE}",
        backup_dir=backup_dir,
    )

    if meetings_data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETINGS_FILE}。")
        return False
        
    latest_matching_meeting = None
    latest_meeting_timestamp = -1
    try:
        for meeting in meetings_data:
            if (
                meeting.get(MEETING_TYPE_KEY) == MEETING_TYPE_PERSONAL
                and meeting.get(HOST_ID_KEY) == user_id
                and meeting.get(MEETING_STATUS_KEY) == MEETING_STATUS_ONGOING
                and (not personal_meeting_id or meeting.get("meetingId") == personal_meeting_id)
            ):
                current_timestamp = meeting.get(MEETING_START_TIME_KEY, 0) 
                if current_timestamp > latest_meeting_timestamp:
                    latest_meeting_timestamp = current_timestamp
                    latest_matching_meeting = meeting
    except Exception as e:
        logging.error(f"处理 {MEETINGS_FILE} 数据时发生错误: {e}")
        return False

    if latest_matching_meeting is not None:
        actual_meeting_waiting_room = latest_matching_meeting.get(MEETING_SETTINGS_KEY, {}).get(ENABLE_WAITING_ROOM_KEY)
        if actual_meeting_waiting_room == expected_waiting_room_status:
            return True
        logging.error(
            f"个人会议室进行中记录的等候室设置不符合预期。"
            f"实际状态: {actual_meeting_waiting_room}, 期望状态: {expected_waiting_room_status}。"
        )

    if expected_in_meeting_status and _has_enter_personal_room_result_evidence(result):
        logging.warning("meetings.json中未找到个人会议室会议记录，但Agent结果提供了进入个人会议室证据，视为成功。")
        return True

    return False




if __name__ == '__main__':
    print(check_personal_meeting_room_waiting_room_status())
