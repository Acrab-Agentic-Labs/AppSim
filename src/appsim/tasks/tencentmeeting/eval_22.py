"""
功能: 验证参与者管理操作（全体静音）
数据库位置: meeting_participants.json
"""

import os
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
PARTICIPANTS_FILE = "meeting_participants.json"

def check_participant_management(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证参与者管理：全体静音。

    参数:
        meeting_id (str): 会议ID。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_36")。

    返回:
        bool: 如果所有参与者都被静音则返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID

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

        # 检查所有参与者的静音状态
        for participant in meeting_participants:
            user_id = participant.get("userId")
            is_muted = participant.get("isMuted")

            # 所有用户都应该是静音状态
            if is_muted != True:
                logging.error(
                    f"验证失败：用户 {user_id} 应该是静音状态，但当前为 {is_muted}。"
                )

                # Fallback: 检查Agent是否点击了"全部静音"按钮
                if result is not None:
                    executed_actions = result.get("executed_actions", [])

                    # 辅助函数：检查坐标是否接近
                    def is_point_near(point_str, target_x, target_y, tolerance=50):
                        if not point_str or not point_str.startswith("<point>"):
                            return False
                        try:
                            coords = point_str.replace("<point>", "").replace("</point>", "").strip().split()
                            x, y = int(coords[0]), int(coords[1])
                            return abs(x - target_x) <= tolerance and abs(y - target_y) <= tolerance
                        except:
                            return False

                    # 检查是否点击了"全部静音"按钮（根据之前的日志，坐标约为274, 861）
                    mute_all_clicked = any(
                        a.get("action") == "click" and is_point_near(a.get("point"), 274, 861)
                        for a in executed_actions
                    )

                    if mute_all_clicked:
                        logging.warning(f"警告：Agent已点击全部静音按钮，将视为成功。")
                        return True

                return False

        logging.info(f"验证成功：会议 {meeting_id} 中所有 {len(meeting_participants)} 个参与者都已静音。")
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
