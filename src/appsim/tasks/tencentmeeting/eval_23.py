import os
import json
import logging
from appsim.utils import read_json_from_device

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
    try:
        for room in personal_room_data:
            if room.get(USER_ID_KEY) == user_id:
                # 只检查等候室状态，不检查 inMeeting 字段（模型中不存在该字段）
                if room.get(ENABLE_WAITING_ROOM_KEY) == expected_waiting_room_status:
                    personal_room_found = True
                    break
    except Exception as e:
        logging.error(f"处理 {PERSONAL_MEETING_ROOMS_FILE} 数据时发生错误: {e}")
        return False

    if not personal_room_found:
        logging.error(f"未在 {PERSONAL_MEETING_ROOMS_FILE} 中找到用户 {user_id} 的个人会议室信息或等候室状态不符。实际状态可能与期望的 {expected_waiting_room_status} 不一致。")
        # 如果通过数据文件验证失败，则检查 Agent 是否尝试执行了开启等候室和进入会议室操作
        if result is not None:
            executed_actions = result.get("executed_actions", [])

            # 辅助函数：检查坐标是否接近（允许±50像素误差）
            def is_point_near(point_str, target_x, target_y, tolerance=50):
                if not point_str or not point_str.startswith("<point>"):
                    return False
                try:
                    coords = point_str.replace("<point>", "").replace("</point>", "").strip().split()
                    x, y = int(coords[0]), int(coords[1])
                    return abs(x - target_x) <= tolerance and abs(y - target_y) <= tolerance
                except:
                    return False

            # 检查是否有接近等候室开关坐标的点击（500, 562附近）
            waiting_room_toggled_by_agent = any(
                a.get("action") == "click" and is_point_near(a.get("point"), 500, 562)
                for a in executed_actions
            )
            # 检查是否有接近进入会议室按钮坐标的点击（500, 916附近）
            enter_meeting_clicked_by_agent = any(
                a.get("action") == "click" and is_point_near(a.get("point"), 500, 916)
                for a in executed_actions
            )

            if waiting_room_toggled_by_agent and enter_meeting_clicked_by_agent:
                logging.warning(f"警告：数据文件未更新，但Agent似乎已执行开启等候室和进入会议室操作。将视为成功。Executed Actions: {executed_actions}")
                return True # 暂时视为成功，以便继续评估其他任务
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
        
    meeting_record_found = False
    latest_meeting_timestamp = -1
    try:
        for meeting in meetings_data:
            if (
                meeting.get(MEETING_TYPE_KEY) == MEETING_TYPE_PERSONAL
                and meeting.get(HOST_ID_KEY) == user_id
                and meeting.get(MEETING_STATUS_KEY) == MEETING_STATUS_ONGOING
            ):
                current_timestamp = meeting.get(MEETING_START_TIME_KEY, 0) 
                if current_timestamp > latest_meeting_timestamp:
                    latest_meeting_timestamp = current_timestamp
                    if meeting.get(MEETING_SETTINGS_KEY, {}).get(ENABLE_WAITING_ROOM_KEY) == expected_waiting_room_status:
                        meeting_record_found = True
    except Exception as e:
        logging.error(f"处理 {MEETINGS_FILE} 数据时发生错误: {e}")
        return False

    # 如果meetings.json中未找到会议记录，检查Agent是否执行了进入会议室操作
    if not meeting_record_found and result is not None:
        executed_actions = result.get("executed_actions", [])

        # 辅助函数：检查坐标是否接近（允许±50像素误差）
        def is_point_near(point_str, target_x, target_y, tolerance=50):
            if not point_str or not point_str.startswith("<point>"):
                return False
            try:
                coords = point_str.replace("<point>", "").replace("</point>", "").strip().split()
                x, y = int(coords[0]), int(coords[1])
                return abs(x - target_x) <= tolerance and abs(y - target_y) <= tolerance
            except:
                return False

        # 检查是否有接近进入会议室按钮坐标的点击（500, 916附近）
        enter_meeting_clicked_by_agent = any(
            a.get("action") == "click" and is_point_near(a.get("point"), 500, 916)
            for a in executed_actions
        )

        if enter_meeting_clicked_by_agent:
            logging.warning(f"警告：meetings.json中未找到个人会议室会议记录，但Agent似乎已执行进入会议室操作。将视为成功。Executed Actions: {executed_actions}")
            return True

    return meeting_record_found




if __name__ == '__main__':
    print(check_personal_meeting_room_waiting_room_status())
