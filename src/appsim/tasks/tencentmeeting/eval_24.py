"""
功能: 统计未开始的会议中设置了密码的会议数量
数据库位置: meetings.json
"""

import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
EXPECTED_COUNT = 8
MEETINGS_FILE = "meetings.json"

def verify_upcoming_meetings_with_password(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证未开始的会议中设置了密码的会议数量。

    参数:
        expected_count (int): 期望的未开始且设置了密码的会议数量。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_30")。

    返回:
        bool: 如果实际数量与期望数量匹配则返回True，否则返回False。
    """

    # 使用常量
    expected_count = EXPECTED_COUNT

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_30")

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
        # 过滤：status == "UPCOMING" 且 password 不为空
        upcoming_meetings = [m for m in meetings_data if m.get("status") == "UPCOMING"]
        meetings_with_password = [m for m in upcoming_meetings if m.get("password")]

        actual_count = len(meetings_with_password)

        if actual_count == expected_count:
            return True
        else:
            logging.error(
                f"验证失败：未开始且设置了密码的会议数量为 {actual_count}，期望为 {expected_count}。"
            )
            return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_30")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: verify_upcoming_meetings_with_password(expected_count=11, backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(verify_upcoming_meetings_with_password())
