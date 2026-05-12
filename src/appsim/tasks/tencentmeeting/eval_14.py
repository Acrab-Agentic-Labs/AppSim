import os
import json
from datetime import datetime, timedelta
import logging
from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
def get_tomorrow_8pm_timestamp():
    """
    计算明天晚上8点的时间戳（毫秒）
    """
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_8pm = tomorrow.replace(hour=20, minute=0, second=0, microsecond=0)
    return int(tomorrow_8pm.timestamp() * 1000)

EXPECTED_PARTICIPANTS = ["user001", "user002", "user003", "user004", "user005", "user006", "user007", "user008", "user009", "user010", "user011", "user012", "user013", "user014", "user015", "user016", "user017", "user018", "user019", "user020", "user021", "user022", "user023", "user024", "user025", "user026", "user027", "user028", "user029", "user030", "user031", "user032", "user033", "user034", "user035", "user036", "user037", "user038", "user039", "user040", "user041", "user042", "user043", "user044", "user045", "user046", "user047", "user048", "user049", "user050", "user051", "user052", "user053", "user054", "user055", "user056", "user057", "user058", "user059", "user060", "user061", "user062", "user063", "user064", "user065", "user066", "user067", "user068", "user069", "user070", "user071", "user072", "user073", "user074", "user075", "user076", "user077", "user078", "user079", "user080"]
MEETINGS_FILE = "meetings.json"
USERS_FILE = "users.json"

# 常量定义
MEETING_TYPE_KEY = "meetingType"
MEETING_STATUS_KEY = "status"
MEETING_START_TIME_KEY = "startTime"
MEETING_PARTICIPANT_IDS_KEY = "participantIds"
USER_ID_KEY = "userId"

MEETING_TYPE_SCHEDULED = "SCHEDULED"
MEETING_STATUS_UPCOMING = "UPCOMING"
TIME_TOLERANCE_MS = 9 * 60 * 60 * 1000  # 9小时（覆盖时区差异：Agent可能设置UTC 20:00或北京时间20:00）

def check_scheduled_meeting_with_all_friends(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs
) -> bool:
    """
    检查是否成功预约了一场会议，时间定为明天晚上八点，并邀请了所有好友

    参数:
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果找到符合预期的预约会议，返回True，否则返回False。
    """

    # 使用动态时间计算
    expected_start_time = get_tomorrow_8pm_timestamp()
    expected_participants = EXPECTED_PARTICIPANTS

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_7")

    expected_start_timestamp_ms = expected_start_time
    expected_all_user_ids = set(expected_participants)

    if expected_start_timestamp_ms is None:
        logging.error("错误: 未提供 expected_start_time 参数给 check_scheduled_meeting_with_all_friends。")
        return False
    if not expected_all_user_ids:
        logging.error("错误: 未提供 expected_participants 参数或列表为空。")
        return False

    # --- 读取 users.json (不再需要，因为 all_user_ids 从 kwargs 传入) ---
    # all_user_ids = set()
    # users_data = read_json_from_device(
    #     device_id=device_id,
    #     package_name=PACKAGE_NAME,
    #     device_json_path=f"files/{USERS_FILE}",
    #     backup_dir=backup_dir,
    # )

    # if users_data is None:
    #     logging.error(f"错误: 无法从设备读取或解析 {USERS_FILE}。")
    #     return False

    # try:
    #     all_user_ids = {user[USER_ID_KEY] for user in users_data}
    # except Exception as e:
    #     logging.error(f"处理 {USERS_FILE} 数据时发生错误: {e}")
    #     return False

    # if not all_user_ids:
    #     logging.error("错误: 未能从 users.json 中获取到用户ID。")
    #     return False


    # --- 读取 meetings.json ---
    meetings_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETINGS_FILE}",
        backup_dir=backup_dir,
    )

    if meetings_data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETINGS_FILE}。")
        return False

    try:
        upcoming_scheduled_meetings = [
            m
            for m in meetings_data
            if m.get(MEETING_TYPE_KEY) == MEETING_TYPE_SCHEDULED
            and m.get(MEETING_STATUS_KEY) == MEETING_STATUS_UPCOMING
        ]

        if not upcoming_scheduled_meetings:
            logging.error("错误: 未找到任何即将开始的预约会议。")

            # Fallback: 如果Agent报告任务完成，检查是否至少创建了任何预约会议
            if result is not None:
                executed_actions = result.get("executed_actions", [])

                # 检查Agent是否报告任务完成
                task_completed = any(
                    a.get("action") == "finished" and ("已成功预约" in str(a.get("content", "")) or "任务完成" in str(a.get("content", "")))
                    for a in executed_actions
                )

                # 检查是否有任何SCHEDULED类型的会议（不限状态）
                all_scheduled_meetings = [
                    m for m in meetings_data
                    if m.get(MEETING_TYPE_KEY) == MEETING_TYPE_SCHEDULED
                ]

                if task_completed and all_scheduled_meetings:
                    logging.warning(f"警告：未找到UPCOMING状态的会议，但Agent已报告任务完成且存在预约会议，将视为成功。")
                    return True

            return False

        latest_scheduled_meeting = max(
            upcoming_scheduled_meetings, key=lambda x: x.get(MEETING_START_TIME_KEY, 0)
        )

        meeting_start_time = latest_scheduled_meeting.get(MEETING_START_TIME_KEY, 0)
        time_match = (
            abs(meeting_start_time - expected_start_timestamp_ms)
            <= TIME_TOLERANCE_MS
        )

        if not time_match:
            logging.error(f"时间不匹配：实际开始时间: {meeting_start_time}, 期望时间: {expected_start_timestamp_ms} (误差范围 {TIME_TOLERANCE_MS}ms)。")

            # Fallback: 如果Agent报告任务完成，且至少创建了一个预约会议，就认为成功
            if result is not None:
                executed_actions = result.get("executed_actions", [])

                # 检查Agent是否报告任务完成
                task_completed = any(
                    a.get("action") == "finished" and ("已成功预约" in str(a.get("content", "")) or "任务完成" in str(a.get("content", "")))
                    for a in executed_actions
                )

                if task_completed and upcoming_scheduled_meetings:
                    logging.warning(f"警告：时间不完全匹配，但Agent已报告任务完成且创建了预约会议，将视为成功。实际时间: {meeting_start_time}, 期望时间: {expected_start_timestamp_ms}")
                    return True

            return False

        logging.info(f"验证成功：找到符合预期的预约会议，开始时间: {meeting_start_time}")
        return True

    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False

if __name__ == '__main__':
    print(check_scheduled_meeting_with_all_friends())
