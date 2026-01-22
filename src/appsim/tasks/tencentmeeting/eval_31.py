"""
功能: 验证参与者管理操作（全体静音、单独解除静音、移出参与者）
数据库位置: meeting_participants.json
"""

import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
UNMUTED_USER_ID = "user003"
REMOVED_USER_ID = ""
PARTICIPANTS_FILE = "meeting_participants.json"

def check_participant_management(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证参与者管理：全体静音、解除指定用户静音、移出指定用户。

    参数:
        meeting_id (str): 会议ID。
        unmuted_user_id (str): 应该被解除静音的用户ID。
        removed_user_id (str): 应该被移出的用户ID。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_36")。

    返回:
        bool: 如果参与者状态符合要求则返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    unmuted_user_id = UNMUTED_USER_ID
    removed_user_id = REMOVED_USER_ID

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_36")

    try:
        participants_data = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{PARTICIPANTS_FILE}",
            backup_dir=backup_dir,
        )
    except FileNotFoundError:
        logging.error(f"错误: 文件在设备上未找到: files/{PARTICIPANTS_FILE}")
        return False
    except Exception as e:
        logging.error(f"从设备读取JSON文件时发生错误: {e}")
        return False

    if participants_data is None:
        logging.error(f"无法从设备读取或解析 {PARTICIPANTS_FILE}。")
        return False

    try:
        # 过滤出指定会议的参与者
        meeting_participants = [p for p in participants_data if p.get("meetingId") == meeting_id]

        if not meeting_participants:
            logging.error(f"会议 {meeting_id} 中没有找到任何参与者。")
            return False

        # 检查被移出的用户不应该在参与者列表中
        if any(p.get("userId") == removed_user_id for p in meeting_participants):
            logging.error(f"验证失败：用户 {removed_user_id} 应该已被移出，但仍在参与者列表中。")
            return False

        # 检查其他参与者的静音状态
        for participant in meeting_participants:
            user_id = participant.get("userId")
            is_muted = participant.get("isMuted")

            if user_id == unmuted_user_id:
                # 这个用户应该是未静音状态
                if is_muted != False:
                    logging.error(
                        f"验证失败：用户 {user_id} 应该是未静音状态，但当前为 {is_muted}。"
                    )
                    return False
            else:
                # 其他用户应该都是静音状态
                if is_muted != True:
                    logging.error(
                        f"验证失败：用户 {user_id} 应该是静音状态，但当前为 {is_muted}。"
                    )
                    return False

        return True

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_36")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: check_participant_management(meeting_id='meeting_3d7e91', unmuted_user_id='user003', removed_user_id='user004', backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(check_participant_management())
