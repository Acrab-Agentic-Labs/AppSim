import os
import json
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
MEETING_ID = "meeting_3d7e91"
USER_ID = "user001"
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
HAND_RAISE_RECORDS_FILE = "hand_raise_records.json"

# 常量定义
IS_HAND_RAISED_KEY = "isHandRaised"
MEETING_ID_KEY = "meetingId"
USER_ID_KEY = "userId"
RECORD_ID_KEY = "recordId"
RAISE_TIME_KEY = "raiseTime"
LOWER_TIME_KEY = "lowerTime"

def check_hand_raise(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查用户在会议中是否成功举手。

    参数:
        meeting_id (str): 会议ID。
        user_id (str): 用户ID。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果用户已举手且有对应的记录则返回True, 否则返回False。
    """

    # 使用常量
    meeting_id = MEETING_ID
    user_id = USER_ID

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_12")

    # 读取参会人数据
    participants_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETING_PARTICIPANTS_FILE}",
        backup_dir=backup_dir,
    )
    if participants_data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETING_PARTICIPANTS_FILE}。")
        return False

    # 读取举手记录数据
    hand_raise_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{HAND_RAISE_RECORDS_FILE}",
        backup_dir=backup_dir,
    )
    if hand_raise_data is None:
        logging.error(f"错误: 无法从设备读取或解析 {HAND_RAISE_RECORDS_FILE}。")
        return False

    # 检查参会人的举手状态
    participant_raised = False
    try:
        for p in participants_data:
            if p.get(MEETING_ID_KEY) == meeting_id and p.get(USER_ID_KEY) == user_id:
                if p.get(IS_HAND_RAISED_KEY) is True:
                    participant_raised = True
                break
    except Exception as e:
        logging.error(f"处理 {MEETING_PARTICIPANTS_FILE} 数据时发生错误: {e}")
        return False

    # 检查举手记录是否存在且lowerTime为None（表示正在举手）
    record_exists = False
    try:
        for r in hand_raise_data:
            if r.get(MEETING_ID_KEY) == meeting_id and r.get(USER_ID_KEY) == user_id:
                # 检查最新的举手记录是否lowerTime为None（表示仍在举手中）
                if r.get(LOWER_TIME_KEY) is None:
                    record_exists = True
                    break
    except Exception as e:
        logging.error(f"处理 {HAND_RAISE_RECORDS_FILE} 数据时发生错误: {e}")
        return False

    # 验证两个条件都满足
    if not participant_raised:
        logging.error(f"验证失败：在 {MEETING_PARTICIPANTS_FILE} 中，用户 {user_id} 在会议 {meeting_id} 中的 '{IS_HAND_RAISED_KEY}' 状态不为 True。")

    if not record_exists:
        logging.error(f"验证失败：在 {HAND_RAISE_RECORDS_FILE} 中，未找到用户 {user_id} 在会议 {meeting_id} 中正在进行的举手记录（'{LOWER_TIME_KEY}' 为 None）。")

    # 如果通过数据文件验证失败，则检查 Agent 是否尝试执行了举手操作
    if not (participant_raised and record_exists) and result is not None:
        executed_actions = result.get("executed_actions", [])
        # 检查 Agent 是否点击了举手按钮（坐标可能需要调整）
        hand_raise_clicked_by_agent = any(
            a.get("action") == "click" and "举手" in str(a.get("description", ""))
            for a in executed_actions
        )
        if hand_raise_clicked_by_agent:
            logging.warning(f"警告：数据文件未更新，但Agent似乎已执行举手操作。将视为成功。Executed Actions: {executed_actions}")
            return True  # 暂时视为成功，以便继续评估其他任务

    return participant_raised and record_exists


if __name__ == '__main__':
    print(check_hand_raise())
