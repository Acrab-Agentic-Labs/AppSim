"""
功能: 统计指定会议中指定用户发送的消息数量
数据库位置: messages.json
"""

import os
import logging
from appsim.utils import read_json_from_device

TASK17_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取指定用户发送的消息数量。",
    "properties": {
        "message_count": {
            "type": "integer",
            "minimum": 0,
            "description": "发送的消息数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["message_count"],
    "additionalProperties": False,
}


PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
SENDER_ID = "user002"
EXPECTED_COUNT = 2
MESSAGES_FILE = "messages.json"

def verify_sender_message_count(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证指定会议中指定用户发送的消息数量。

    参数:
        meeting_id (str): 会议ID。
        sender_id (str): 发送者用户ID。
        expected_count (int): 期望的消息数量。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_32")。

    返回:
        bool: 如果实际消息数量与期望数量匹配则返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    sender_id = SENDER_ID
    expected_count = EXPECTED_COUNT

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_32")

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

        # 再过滤出指定发送者的消息
        sender_messages = [m for m in meeting_messages if m.get("senderId") == sender_id]

        actual_count = len(sender_messages)

        if actual_count != expected_count:
            logging.error(
                "Sender %s in meeting %s sent %s messages, expected %s.",
                sender_id,
                meeting_id,
                actual_count,
                expected_count,
            )
            return False

        if not isinstance(result, dict):
            return False
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict) and extracted_answer.get("message_count") == actual_count:
            return True
        return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_32")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: verify_message_count_by_sender(meeting_id='meeting_3d7e91', sender_id='user002', expected_count=2, backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(verify_sender_message_count())
