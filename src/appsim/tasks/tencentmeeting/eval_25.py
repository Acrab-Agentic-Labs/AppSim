"""
功能: 查找指定用户创建的会议中参与人数最多的会议主题
数据库位置: meetings.json
"""

import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
HOST_ID = "user002"
EXPECTED_TOPIC = "技术方案讨论"
MEETINGS_FILE = "meetings.json"

def verify_chensiyuan_max_participants_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证指定用户创建的所有会议中，参与人数最多的会议主题。

    参数:
        expected_topic (str): 期望的会议主题。
        host_id (str): 创建会议的用户ID。默认为user002（陈思远）。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_31")。

    返回:
        bool: 如果实际会议主题与期望主题匹配则返回True，否则返回False。
    """

    # 使用常量
    host_id = HOST_ID
    expected_topic = EXPECTED_TOPIC

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_31")

    try:
        meetings_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{MEETINGS_FILE}",
            backup_dir=backup_dir,
        )
    except FileNotFoundError:
        logging.error(f"错误: 文件在设备上未找到: files/{MEETINGS_FILE}")
        return False
    except Exception as e:
        logging.error(f"从设备读取JSON文件时发生错误: {e}")
        return False

    if meetings_data is None:
        logging.error(f"无法从设备读取或解析 {MEETINGS_FILE}。")
        return False

    try:
        # 过滤出指定用户创建的会议
        user_meetings = [m for m in meetings_data if m.get("hostId") == host_id]

        if not user_meetings:
            logging.error(f"未找到用户 {host_id} 创建的会议。")
            return False

        # 找到参与人数最多的会议
        max_meeting = max(user_meetings, key=lambda m: len(m.get("participantIds", [])))
        actual_topic = max_meeting.get("topic")

        if actual_topic == expected_topic:
            return True
        else:
            logging.error(
                f"验证失败：参与人数最多的会议主题为 '{actual_topic}'，期望为 '{expected_topic}'。"
            )
            return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_31")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: verify_chensiyuan_max_participants_meeting(expected_topic='技术方案讨论', backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(verify_chensiyuan_max_participants_meeting())
