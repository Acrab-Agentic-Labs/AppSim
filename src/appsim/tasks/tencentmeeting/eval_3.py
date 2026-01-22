import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "341234546"
PASSWORD = "312435"
USER_ID = "user001"
MEETINGS_FILE = "meetings.json"
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"

# 常量定义
MEETING_ID_KEY = "meetingId"
MEETING_PASSWORD_KEY = "password"
USER_ID_KEY = "userId"

def check_join_meeting_with_password(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查用户是否通过正确的会议号和密码成功加入会议，并在数据库中记录。

    参数:
        meeting_id (str): 会议ID (会议号)。
        password (str): 会议密码。
        user_id (str): 加入会议的用户ID。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果会议存在、密码正确且用户已加入则返回True, 否则返回False。
    """
    # 使用常量
    meeting_id = MEETING_ID
    password = PASSWORD
    user_id = USER_ID
    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_9")

    meetings_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETINGS_FILE}",
        backup_dir=backup_dir,
    )

    if meetings_data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETINGS_FILE}。")
        return False

    meeting_found = False
    try:
        for meeting in meetings_data:
            if meeting.get(MEETING_ID_KEY) == meeting_id:
                if meeting.get(MEETING_PASSWORD_KEY) == password:
                    meeting_found = True
                    break
                else:
                    logging.error(f"会议 {meeting_id} 密码错误。")
                    return False  # 密码错误

        if not meeting_found:
            logging.error(f"未找到会议 {meeting_id}。")
            return False  # 会议不存在

    except Exception as e:
        logging.error(f"处理 {MEETINGS_FILE} 数据时发生错误: {e}")
        return False

    participants_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETING_PARTICIPANTS_FILE}",
        backup_dir=backup_dir,
    )

    if participants_data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETING_PARTICIPANTS_FILE}。")
        return False

    try:
        # 检查特定用户是否已加入会议
        for participant in participants_data:
            if (
                participant.get(USER_ID_KEY) == user_id
                and participant.get(MEETING_ID_KEY) == meeting_id
            ):
                return True
        
        logging.error(f"用户 {user_id} 未加入会议 {meeting_id}。")
        return False  # 用户未加入会议

    except Exception as e:
        logging.error(f"处理 {MEETING_PARTICIPANTS_FILE} 数据时发生错误: {e}")
        return False

if __name__ == '__main__':
    print(check_join_meeting_with_password())
