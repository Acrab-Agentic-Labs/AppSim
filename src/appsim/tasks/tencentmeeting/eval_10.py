"""
功能: 验证技术讨论会议中可邀请的人员数量
"""

import logging
import os
from appsim.utils import read_json_from_device
try:
    from ._answer_utils import answer_contains_any, answer_contains_number
except ImportError:
    from _answer_utils import answer_contains_any, answer_contains_number


PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
EXPECTED_COUNT = 32
USERS_FILE = "users.json"
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
USER_ID_KEY = "userId"


def verify_invitable_people_count(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证会议中可邀请的人员数量是否与预期匹配。

    参数:
        expected_count (int): 期望的可邀请人员数量。
        meeting_id (str, optional): 会议ID（未使用，保留以兼容）。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果实际可邀请人数与期望数目匹配则返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    expected_count = EXPECTED_COUNT

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_reasoning_tasks")

    users_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{USERS_FILE}",
        backup_dir=backup_dir,
    )
    if users_data is None:
        print(f"错误: 无法从设备读取或解析 {USERS_FILE}。")
        return False

    participants_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETING_PARTICIPANTS_FILE}",
        backup_dir=backup_dir,
    )
    if participants_data is None:
        print(f"错误: 无法从设备读取或解析 {MEETING_PARTICIPANTS_FILE}。")
        return False

    all_user_ids = {user.get(USER_ID_KEY) for user in users_data if user.get(USER_ID_KEY)}
    current_meeting_participant_ids = {p.get(USER_ID_KEY) for p in participants_data if p.get(USER_ID_KEY)}

    # 可邀请人数 = 总用户数 - 已在会议中的用户数
    actual_count = len(all_user_ids - current_meeting_participant_ids)
    if actual_count != expected_count:
        logging.error("Invitable count %s did not match expected %s.", actual_count, expected_count)
        return False

    return answer_contains_number(result, actual_count)


if __name__ == '__main__':
    print(verify_invitable_people_count())
