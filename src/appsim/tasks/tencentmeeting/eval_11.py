import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
IS_MUTED_KEY = "isMuted"

def check_all_mics_muted(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查指定会议中所有用户的麦克风是否都已关闭（静音）。

    参数:
        meeting_id (str): 会议ID。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果指定会议中所有用户的麦克风都已关闭，返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_4")

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
        meeting_participants = [
            p for p in data if p.get("meetingId") == meeting_id
        ]

        if not meeting_participants:
            logging.error(f"会议 {meeting_id} 没有找到参与者记录，默认为验证失败。")
            return False

        for participant in meeting_participants:
            if participant.get(IS_MUTED_KEY) is False:
                logging.error(f"验证失败：会议 {meeting_id} 中的参与者 {participant.get('userId')} 的麦克风未关闭。")
                return False

        return True

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == '__main__':
    print(check_all_mics_muted())
