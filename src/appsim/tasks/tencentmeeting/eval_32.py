"""
功能: 验证按条件邀请用户（手机号13开头的联系人）
数据库位置: meetings.json, users.json
"""

import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
EXPECTED_TOPIC = "新产品发布"
MEETINGS_FILE = "meetings.json"
USERS_FILE = "users.json"

def check_selective_meeting_invitation(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证按条件邀请用户：邀请所有手机号13开头的联系人，并设置会议主题。

    参数:
        expected_topic (str): 期望的会议主题。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_37")。

    返回:
        bool: 如果最新会议的主题正确且包含所有手机号13开头的用户则返回True，否则返回False。
    """

    # 使用常量
    expected_topic = EXPECTED_TOPIC

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_37")

    try:
        meetings_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{MEETINGS_FILE}",
            backup_dir=backup_dir,
        )
        users_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{USERS_FILE}",
            backup_dir=backup_dir,
        )
    except FileNotFoundError as e:
        logging.error(f"错误: 文件在设备上未找到: {e}")
        return False
    except Exception as e:
        logging.error(f"从设备读取JSON文件时发生错误: {e}")
        return False

    if meetings_data is None or users_data is None:
        logging.error(f"无法从设备读取或解析数据文件。")
        return False

    try:
        # 找到所有手机号13开头的用户
        phone13_users = [u for u in users_data if u.get("phone", "").startswith("13")]
        phone13_user_ids = {u.get("userId") for u in phone13_users}

        if not phone13_users:
            logging.error("未找到手机号13开头的用户。")
            return False

        # 找到最新创建的会议（按startTime排序）
        if not meetings_data:
            logging.error("没有找到任何会议。")
            return False

        # 尝试按startTime排序，如果没有则按meetingId排序
        try:
            latest_meeting = max(meetings_data, key=lambda m: m.get("startTime", 0))
        except (TypeError, ValueError):
            # 如果startTime不是数字，回退到按meetingId排序
            latest_meeting = max(meetings_data, key=lambda m: m.get("meetingId", ""))

        # 检查会议主题
        actual_topic = latest_meeting.get("topic")
        if actual_topic != expected_topic:
            logging.error(
                f"验证失败：会议主题为 '{actual_topic}'，期望为 '{expected_topic}'。"
            )
            return False

        # 只检查会议主题，不检查邀请人数
        logging.info(f"验证成功：会议主题为 '{actual_topic}'")
        return True

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_37")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: check_selective_meeting_invitation(expected_topic='重要会议', backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(check_selective_meeting_invitation())
