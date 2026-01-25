import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
USER_ID = "user001"
EXPECTED_STATUS = True
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
IS_CAMERA_ON_KEY = "isCameraOn"

def check_camera_enabled(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查指定会议中特定用户的摄像头状态。

    参数:
        meeting_id (str): 会议ID。
        user_id (str): 用户ID。
        expected_status (bool): 期望的摄像头状态 (True为打开, False为关闭)。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果摄像头状态符合预期，返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    user_id = USER_ID
    expected_status = EXPECTED_STATUS

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_2")

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
        for participant in data:
            if participant.get("meetingId") == meeting_id and participant.get("userId") == user_id:
                return participant.get(IS_CAMERA_ON_KEY) == expected_status
        
        logging.error(f"未在 {MEETING_PARTICIPANTS_FILE} 中找到会议 {meeting_id} 的参与者 {user_id}。")
        return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == '__main__':
    print(check_camera_enabled())
