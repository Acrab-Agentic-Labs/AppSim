import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
EXPECTED_MEETING_ID = "meeting_4e8d73"
MEETINGS_FILE = "meetings.json"

# 常量定义
MEETING_STATUS_KEY = "status"
MEETING_END_TIME_KEY = "endTime"
MEETING_ID_KEY = "meetingId"
MEETING_STATUS_ENDED = "ENDED"

def check_previous_meeting_playback(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查最近一场已结束的会议ID是否与期望值匹配，用于验证回放。

    参数:
        expected_meeting_id (str): 期望的会议ID。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果最近结束的会议ID与期望的ID匹配，返回True，否则返回False。
    """
    # 使用常量
    expected_meeting_id = EXPECTED_MEETING_ID
    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_8")

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
        ended_meetings = [
            m for m in data if m.get(MEETING_STATUS_KEY) == MEETING_STATUS_ENDED and m.get(MEETING_END_TIME_KEY) is not None
        ]

        if not ended_meetings:
            logging.error("错误: 未找到任何已结束的会议。")
            return False

        previous_meeting = max(ended_meetings, key=lambda x: x.get(MEETING_END_TIME_KEY, 0))

        actual_meeting_id = previous_meeting.get(MEETING_ID_KEY)
        if actual_meeting_id == expected_meeting_id:
            return True
        else:
            logging.error(f"验证失败：最近的会议ID '{actual_meeting_id}' 与期望的ID '{expected_meeting_id}' 不匹配。")
            return False

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False

if __name__ == '__main__':
    print(check_previous_meeting_playback())
