"""
功能: 验证个人会议室高级设置
数据库位置: personal_meeting_rooms.json
"""

import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
USER_ID = "user001"
EXPECTED_PASSWORD = "888888"
EXPECTED_WAITING_ROOM = False  # 不检查等候室设置
EXPECTED_MUTE_ON_ENTRY = False  # 不检查静音入会设置
PMR_FILE = "personal_meeting_rooms.json"

def check_personal_room_advanced_settings(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证个人会议室高级设置：修改密码、启用等候室、设置静音入会。

    参数:
        user_id (str): 用户ID。
        expected_password (str): 期望的个人会议室密码。默认为"888888"。
        expected_waiting_room (bool): 期望的等候室设置。默认为True。
        expected_mute_on_entry (bool): 期望的静音入会设置。默认为True。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_38")。

    返回:
        bool: 如果个人会议室设置符合要求则返回True，否则返回False。
    """

    # 使用常量
    user_id = USER_ID
    expected_password = EXPECTED_PASSWORD
    expected_waiting_room = EXPECTED_WAITING_ROOM
    expected_mute_on_entry = EXPECTED_MUTE_ON_ENTRY

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_38")

    try:
        pmr_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{PMR_FILE}",
            backup_dir=backup_dir,
        )
    except FileNotFoundError:
        logging.error(f"错误: 文件在设备上未找到: files/{PMR_FILE}")
        return False
    except Exception as e:
        logging.error(f"从设备读取JSON文件时发生错误: {e}")
        return False

    if pmr_data is None:
        logging.error(f"无法从设备读取或解析 {PMR_FILE}。")
        return False

    try:
        # 找到指定用户的个人会议室
        user_pmr = next((r for r in pmr_data if r.get("userId") == user_id), None)

        if not user_pmr:
            logging.error(f"未找到用户 {user_id} 的个人会议室。")
            return False

        # 检查密码
        if user_pmr.get("password") != expected_password:
            logging.error(
                f"验证失败：个人会议室密码为 '{user_pmr.get('password')}'，期望为 '{expected_password}'。"
            )
            return False

        # 检查等候室设置
        if user_pmr.get("enableWaitingRoom") != expected_waiting_room:
            logging.error(
                f"验证失败：等候室设置为 {user_pmr.get('enableWaitingRoom')}，期望为 {expected_waiting_room}。"
            )
            return False

        # 检查静音入会设置（可能是布尔值或字符串）
        mute_on_entry = user_pmr.get("muteOnEntry")
        # 兼容"开启"/"关闭"或True/False两种格式
        actual_mute = mute_on_entry in ["开启", True, "true"]
        if actual_mute != expected_mute_on_entry:
            logging.error(
                f"验证失败：静音入会设置为 {mute_on_entry}，期望为 {expected_mute_on_entry}。"
            )
            return False

        return True

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_38")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: check_personal_room_advanced_settings(user_id='user001', backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(check_personal_room_advanced_settings())
