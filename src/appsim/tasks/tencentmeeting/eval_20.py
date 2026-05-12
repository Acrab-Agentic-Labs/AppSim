import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
USER_ID = "user001"
EXPECTED_PASSWORD = "648723"
EXPECTED_ENABLE_PASSWORD = True
EXPECTED_WAITING_ROOM = True
EXPECTED_MUTE_ON_ENTRY = "关闭"
CHECK_INVITATIONS = False
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


def _normalize_mute_on_entry(value):
    normalized = str(value).strip().casefold()
    if normalized in {"off", "关闭", "始终关闭"}:
        return "off"
    return normalized


def check_personal_meeting_room_settings(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证个人会议室的设置是否正确（密码、等候室、静音规则）以及是否邀请了周姓好友。

    参数:
        user_id (str): 用户ID，默认"user001"
        expected_password (str): 期望的密码，默认"648723"
        expected_enable_password (bool): 期望密码是否启用，默认True
        expected_waiting_room (bool): 期望等候室是否启用，默认True
        expected_mute_on_entry (str): 期望的入会静音规则，默认"关闭"（选项："关闭"、"超过6人后自动开启"、"始终开启"）
        check_invitations (bool): 是否检查周姓好友的邀请，默认True
        device_id (str): 设备ID
        backup_dir (str): 备份目录

    返回:
        bool: 如果个人会议室设置符合所有期望则返回True，否则返回False
    """

    # 使用常量
    user_id = USER_ID
    expected_password = EXPECTED_PASSWORD
    expected_enable_password = EXPECTED_ENABLE_PASSWORD
    expected_waiting_room = EXPECTED_WAITING_ROOM
    expected_mute_on_entry = EXPECTED_MUTE_ON_ENTRY
    check_invitations = CHECK_INVITATIONS

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_29")

    try:
        # 从设备读取个人会议室数据
        personal_rooms_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{PERSONAL_MEETING_ROOMS_FILE}",
            backup_dir=backup_dir,
        )

        if personal_rooms_data is None:
            logging.error(f"错误: 无法从设备读取或解析 {PERSONAL_MEETING_ROOMS_FILE}。")
            return False

        # 查找指定用户的个人会议室
        user_room = None
        for room in personal_rooms_data:
            if room.get("userId") == user_id:
                user_room = room
                break

        if user_room is None:
            logging.error(f"未找到用户 {user_id} 的个人会议室。")
            return False

        # 保存个人会议室ID，后续检查邀请时需要用到
        personal_meeting_id = user_room.get("meetingId")

        # 验证密码
        actual_password = user_room.get("password")
        if actual_password != expected_password:
            logging.error(
                f"验证失败：个人会议室密码为 '{actual_password}'，期望为 '{expected_password}'。"
            )
            return False

        # 验证密码是否启用
        actual_enable_password = user_room.get("enablePassword", False)
        if actual_enable_password != expected_enable_password:
            logging.error(
                f"验证失败：密码启用状态为 {actual_enable_password}，期望为 {expected_enable_password}。"
            )
            return False

        # 验证等候室
        actual_waiting_room = user_room.get("enableWaitingRoom", False)
        if actual_waiting_room != expected_waiting_room:
            logging.error(
                f"验证失败：等候室设置为 {actual_waiting_room}，期望为 {expected_waiting_room}。"
            )
            return False

        # 验证入会静音规则
        actual_mute_on_entry = user_room.get("muteOnEntry", "")
        if _normalize_mute_on_entry(actual_mute_on_entry) != _normalize_mute_on_entry(expected_mute_on_entry):
            logging.error(
                f"验证失败：成员入会时静音设置为 '{actual_mute_on_entry}'，期望为 '{expected_mute_on_entry}'。"
            )
            return False

        logging.info(f"✅ 个人会议室设置验证成功：")
        logging.info(f"   密码: {actual_password} (启用: {actual_enable_password})")
        logging.info(f"   等候室: {actual_waiting_room}")
        logging.info(f"   入会静音: {actual_mute_on_entry}")

        # 如果需要检查邀请记录
        if check_invitations:
            # 读取用户数据，获取所有周姓用户
            users_data = read_json_from_device(
                device_id=device_id,
                package_name=PACKAGE_NAME,
                device_json_path=f"files/{USERS_FILE}",
                backup_dir=backup_dir,
            )

            if users_data is None:
                logging.error(f"错误: 无法从设备读取或解析 {USERS_FILE}。")
                return False

            # 找出所有周姓用户
            zhou_users = [u for u in users_data if u.get("username", "").startswith("周")]
            zhou_user_ids = {u.get("userId") for u in zhou_users}

            if not zhou_users:
                logging.error("未找到周姓用户。")
                return False

            logging.info(f"找到 {len(zhou_users)} 个周姓用户: {zhou_user_ids}")

            # 读取邀请记录
            invitations_data = read_json_from_device(
                device_id=device_id,
                package_name=PACKAGE_NAME,
                device_json_path=f"files/{INVITATIONS_FILE}",
                backup_dir=backup_dir,
            )

            if invitations_data is None:
                logging.error(f"错误: 无法从设备读取或解析 {INVITATIONS_FILE}。")
                return False

            # 检查是否邀请了所有周姓用户到个人会议室
            invited_zhou_users = set()
            for invitation in invitations_data:
                # 检查邀请记录是否是针对个人会议室的
                if invitation.get("meetingId") == personal_meeting_id:
                    invited_user_id = invitation.get("invitedUserId")
                    if invited_user_id in zhou_user_ids:
                        invited_zhou_users.add(invited_user_id)

            # 检查是否所有周姓用户都被邀请了
            if not zhou_user_ids.issubset(invited_zhou_users):
                missing_users = zhou_user_ids - invited_zhou_users
                logging.error(
                    f"验证失败：部分周姓用户未被邀请到个人会议室。缺失的用户ID: {missing_users}。"
                )
                return False

            logging.info(f"✅ 邀请验证成功：所有 {len(zhou_users)} 个周姓用户都已被邀请。")

        logging.info(f"✅ 所有验证通过！")
        return True

    except Exception as e:
        logging.error(f"验证过程中发生错误: {e}")
        return False

if __name__ == '__main__':
    print(check_personal_meeting_room_settings())
