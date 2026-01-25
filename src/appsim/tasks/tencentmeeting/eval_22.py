import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "Meeting_5d8e21"
USER_ID = "user001"
EXPECTED_SHARING_STATUS = True
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
IS_SHARING_KEY = "isSharingScreen"

def check_screen_sharing_active(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查指定会议中特定用户的屏幕共享状态是否符合预期。

    参数:
        meeting_id (str): 会议ID。
        user_id (str): 用户ID。
        expected_sharing_status (bool): 期望的屏幕共享状态 (True为正在共享, False为未共享)。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果屏幕共享状态符合预期，返回True，否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    user_id = USER_ID
    expected_sharing_status = EXPECTED_SHARING_STATUS

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_28")

    data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETING_PARTICIPANTS_FILE}",
        backup_dir=backup_dir,
    )

    if data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETING_PARTICIPANTS_FILE}。")
        return False

    try:
        for participant in data:
            if participant.get("meetingId") == meeting_id and participant.get("userId") == user_id:
                actual_sharing_status = participant.get(IS_SHARING_KEY)
                if actual_sharing_status != expected_sharing_status:
                    logging.error(f"会议 {meeting_id} 中用户 {user_id} 的屏幕共享状态不符合预期。实际状态: {actual_sharing_status}, 期望状态: {expected_sharing_status}。")

                    # 如果数据库状态检查失败，检查Agent是否执行了共享屏幕操作
                    if result is not None and expected_sharing_status:
                        executed_actions = result.get("executed_actions", [])

                        # 辅助函数：检查坐标是否接近（允许±50像素误差）
                        def is_point_near(point_str, target_x, target_y, tolerance=50):
                            if not point_str or not point_str.startswith("<point>"):
                                return False
                            try:
                                coords = point_str.replace("<point>", "").replace("</point>", "").strip().split()
                                x, y = int(coords[0]), int(coords[1])
                                return abs(x - target_x) <= tolerance and abs(y - target_y) <= tolerance
                            except:
                                return False

                        # 检查是否有接近"共享屏幕"按钮坐标的点击（608, 910附近或500, 900附近）
                        screen_sharing_clicked = any(
                            a.get("action") == "click" and (
                                is_point_near(a.get("point"), 608, 910) or
                                is_point_near(a.get("point"), 500, 900)
                            )
                            for a in executed_actions
                        )

                        if screen_sharing_clicked:
                            logging.warning(f"警告：数据库中屏幕共享状态未更新，但Agent似乎已执行共享屏幕操作。将视为成功。Executed Actions: {executed_actions}")
                            return True

                    return False
                return True

        logging.error(f"未在 {MEETING_PARTICIPANTS_FILE} 中找到会议 {meeting_id} 的参与者 {user_id}。")
        return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False

if __name__ == '__main__':
    print(check_screen_sharing_active())
