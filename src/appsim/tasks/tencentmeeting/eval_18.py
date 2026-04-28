import os
import json
import logging
from appsim.utils import read_json_from_device
try:
    from ._answer_utils import answer_contains_any, answer_contains_number
except ImportError:
    from _answer_utils import answer_contains_any, answer_contains_number


PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
EXPECTED_CONTENT = "大家好"
CURRENT_USER_ID = "user001"
MESSAGES_FILE = "messages.json"
MESSAGE_CONTENT_KEY = "content"
MESSAGE_TIMESTAMP_KEY = "timestamp"

def check_message_content(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查指定会议中最新发送的消息是否包含特定内容。

    参数:
        meeting_id (str): 会议ID。
        expected_content (str): 期望消息的内容。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果在指定会议中最新的消息包含符合预期的内容，返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    expected_content = EXPECTED_CONTENT

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_5")

    data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MESSAGES_FILE}",
        backup_dir=backup_dir,
    )

    if data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MESSAGES_FILE}。")
        return False

    try:
        latest_message = None
        latest_timestamp = -1

        meeting_messages = [msg for msg in data if msg.get("meetingId") == meeting_id]

        if not meeting_messages:
            logging.error("Meeting %s has no messages.", meeting_id)
            return False

        for message in meeting_messages:
            current_timestamp = message.get(MESSAGE_TIMESTAMP_KEY, 0)
            if current_timestamp > latest_timestamp:
                latest_timestamp = current_timestamp
                latest_message = message

        if latest_message is None:
            return False

        actual_content = latest_message.get(MESSAGE_CONTENT_KEY, "")
        actual_sender = latest_message.get("senderId")
        if actual_sender != CURRENT_USER_ID or expected_content not in actual_content:
            logging.error(
                "Latest message sender/content mismatch: sender=%r content=%r expected_sender=%r expected_content=%r.",
                actual_sender,
                actual_content,
                CURRENT_USER_ID,
                expected_content,
            )
            return False

        return answer_contains_any(
            result,
            [
                expected_content,
                "\u5df2\u53d1\u9001",
                "\u53d1\u9001\u6210\u529f",
                "\u6210\u529f\u53d1\u9001",
            ],
        )

    except Exception as e:
        logging.error(f"Error while processing data: {e}")
        return False


if __name__ == '__main__':
    print(check_message_content())
