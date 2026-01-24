import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"
MEETINGS_FILE = "meetings.json"

# 常量定义
MEETING_STATUS_KEY = "status"
MEETING_END_TIME_KEY = "endTime"
MEETING_STATUS_ENDED = "ENDED"

def check_recent_ended_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查是否成功获取到最近结束的会议记录。

    参数:
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果成功获取到至少一个最近结束的会议记录，返回True，否则返回False。
    """
    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_3")

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
            return False # 没有找到任何已结束的会议

        # 找到最近结束的会议 (即使不返回具体ID，只要能找到就认为是成功)
        _ = max(ended_meetings, key=lambda x: x[MEETING_END_TIME_KEY])

        return True # 成功获取到最近结束的会议记录

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == '__main__':
    print(check_recent_ended_meeting())
