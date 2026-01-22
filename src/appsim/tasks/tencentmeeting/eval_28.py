"""
功能: 查找指定会议中发送消息最多的用户
数据库位置: messages.json
"""

import os
import logging
from collections import Counter
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
EXPECTED_SENDER_ID = "user002"
MESSAGES_FILE = "messages.json"

def verify_most_active_sender(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证指定会议中发送消息最多的用户。

    参数:
        meeting_id (str): 会议ID。
        expected_sender_id (str): 期望的最活跃发送者ID。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_34")。

    返回:
        bool: 如果实际最活跃发送者与期望的发送者ID匹配则返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    expected_sender_id = EXPECTED_SENDER_ID

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_34")

    try:
        messages_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{MESSAGES_FILE}",
            backup_dir=backup_dir,
        )
    except FileNotFoundError:
        logging.error(f"错误: 文件在设备上未找到: files/{MESSAGES_FILE}")
        return False
    except Exception as e:
        logging.error(f"从设备读取JSON文件时发生错误: {e}")
        return False

    if messages_data is None:
        logging.error(f"无法从设备读取或解析 {MESSAGES_FILE}。")
        return False

    try:
        # 过滤出指定会议的消息
        meeting_messages = [m for m in messages_data if m.get("meetingId") == meeting_id]

        if not meeting_messages:
            logging.error(f"会议 {meeting_id} 中没有找到任何消息。")
            return False

        # 统计每个发送者的消息数量
        sender_counts = Counter(m.get("senderId") for m in meeting_messages)

        # 找出发送消息最多的用户
        most_active = sender_counts.most_common(1)[0][0]

        if most_active == expected_sender_id:
            return True
        else:
            most_active_count = sender_counts[most_active]
            logging.error(
                f"验证失败：会议 {meeting_id} 中发送消息最多的用户是 {most_active}（{most_active_count}条），期望为 {expected_sender_id}。"
            )
            return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_34")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: verify_most_active_sender(meeting_id='meeting_3d7e91', expected_sender_id='user003', backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(verify_most_active_sender())
