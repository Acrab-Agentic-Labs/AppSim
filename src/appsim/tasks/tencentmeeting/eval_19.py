import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
USER_ID = "user001"
MEETINGS_FILE = "meetings.json"

# 常量定义
MEETING_TYPE_KEY = "meetingType"
MEETING_STATUS_KEY = "status"
MEETING_TOPIC_KEY = "topic"
MEETING_SETTINGS_KEY = "settings"
MEETING_START_TIME_KEY = "startTime"

MEETING_TYPE_INSTANT = "INSTANT"
MEETING_STATUS_ONGOING = "ONGOING"
DEFAULT_QUICK_MEETING_TOPIC = "快速会议"
DEFAULT_QUICK_MEETING_SETTINGS = {
    "allowParticipantUnmute": True,
    "cameraOffOnEntry": True,
    "enableWaitingRoom": False,
    "muteOnEntry": True,
}

def check_quick_meeting_created(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查是否成功创建了一场默认配置的快速会议。

    参数:
        expected_topic (str): 快速会议的默认主题。
        expected_settings (dict, optional): 快速会议的默认设置。如果为None，则使用预设的默认值。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_6")。

    返回:
        bool: 如果找到一场符合默认配置的快速会议，返回True，否则返回False。
    """

    # 使用常量
    user_id = USER_ID
    expected_settings = DEFAULT_QUICK_MEETING_SETTINGS
    expected_topic = DEFAULT_QUICK_MEETING_TOPIC

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_6")

    data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETINGS_FILE}",
        backup_dir=backup_dir,
    )

    if data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETINGS_FILE}。")
        return False

    try:
        # 筛选出所有进行中的快速会议
        ongoing_instant_meetings = [
            m
            for m in data
            if m.get(MEETING_TYPE_KEY) == MEETING_TYPE_INSTANT
            and m.get(MEETING_STATUS_KEY) == MEETING_STATUS_ONGOING
        ]

        if not ongoing_instant_meetings:
            logging.error(f"未找到任何进行中的快速会议。")
            return False

        # 找到最新创建的快速会议 (根据 startTime 判断)
        latest_quick_meeting = max(
            ongoing_instant_meetings, key=lambda x: x.get(MEETING_START_TIME_KEY, 0)
        )

        # 检查主题和设置是否符合默认配置
        topic_match = latest_quick_meeting.get(MEETING_TOPIC_KEY) == expected_topic
        settings_match = latest_quick_meeting.get(MEETING_SETTINGS_KEY) == expected_settings

        if not (topic_match and settings_match):
            logging.error(f"最新快速会议的主题或设置不符合预期。实际主题: {latest_quick_meeting.get(MEETING_TOPIC_KEY)}, 期望主题: {expected_topic}. 实际设置: {latest_quick_meeting.get(MEETING_SETTINGS_KEY)}, 期望设置: {expected_settings}.")
            return False

        return True

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False

if __name__ == '__main__':
    print(check_quick_meeting_created())
