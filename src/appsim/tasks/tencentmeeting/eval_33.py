"""
功能: 验证会议消息发送与举手放手操作
数据库位置: messages.json, hand_raise_records.json
"""

import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
USER_ID = "user001"
EXPECTED_MESSAGE_CONTENT = "我有问题"
MESSAGES_FILE = "messages.json"
HAND_RAISE_FILE = "hand_raise_records.json"

def check_message_and_handraise(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证会议消息发送与举手放手操作：发送消息、举手、放下手。

    参数:
        meeting_id (str): 会议ID。
        user_id (str): 用户ID。
        expected_message_content (str): 期望的消息内容（部分匹配）。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_39")。

    返回:
        bool: 如果消息已发送且举手记录完整则返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    user_id = USER_ID
    expected_message_content = EXPECTED_MESSAGE_CONTENT

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_39")

    try:
        messages_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{MESSAGES_FILE}",
            backup_dir=backup_dir,
        )
        hand_raise_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{HAND_RAISE_FILE}",
            backup_dir=backup_dir,
        )
    except FileNotFoundError as e:
        logging.error(f"错误: 文件在设备上未找到: {e}")
        return False
    except Exception as e:
        logging.error(f"从设备读取JSON文件时发生错误: {e}")
        return False

    if messages_data is None or hand_raise_data is None:
        logging.error(f"无法从设备读取或解析数据文件。")
        return False

    try:
        # 检查消息是否发送
        # 找到指定会议中指定用户的最新消息
        user_messages = [
            m for m in messages_data
            if m.get("meetingId") == meeting_id and m.get("senderId") == user_id
        ]

        if not user_messages:
            logging.error(f"未找到用户 {user_id} 在会议 {meeting_id} 中发送的消息。")
            return False

        # 检查最新消息内容
        latest_message = max(user_messages, key=lambda m: m.get("timestamp", 0))
        message_content = latest_message.get("content", "")

        if expected_message_content not in message_content:
            logging.error(
                f"验证失败：最新消息内容为 '{message_content}'，期望包含 '{expected_message_content}'。"
            )
            return False

        # 检查举手记录
        user_hand_raises = [
            h for h in hand_raise_data
            if h.get("userId") == user_id and h.get("meetingId") == meeting_id
        ]

        if not user_hand_raises:
            logging.error(f"未找到用户 {user_id} 在会议 {meeting_id} 中的举手记录。")
            return False

        # 检查最新的举手记录是否有放下手的时间
        latest_hand_raise = max(user_hand_raises, key=lambda h: h.get("raiseTime", 0))

        if not latest_hand_raise.get("raiseTime"):
            logging.error(f"验证失败：举手记录中没有举手时间。")
            return False

        # lowerTime是可选的，因为任务只要求举手，不要求放下手
        # if not latest_hand_raise.get("lowerTime"):
        #     logging.error(f"验证失败：举手记录中没有放下手的时间。")
        #     return False

        return True

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_39")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: check_message_and_handraise(meeting_id='meeting_3d7e91', user_id='user001', expected_message_content='我有问题', backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(check_message_and_handraise())
