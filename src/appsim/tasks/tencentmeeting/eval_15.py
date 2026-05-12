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
EXPECTED_TOPIC = "客户演示会议"
EXPECTED_DURATION_MINUTES = 60
MEETINGS_FILE = "meetings.json"

# 常量定义
MEETING_STATUS_KEY = "status"
MEETING_END_TIME_KEY = "endTime"
MEETING_START_TIME_KEY = "startTime"
MEETING_TOPIC_KEY = "topic"
MEETING_STATUS_ENDED = "ENDED"

DEFAULT_DURATION_TOLERANCE_MINUTES = 5 # 默认时长容差为5分钟

def get_latest_ended_meeting_details(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查最近一场已结束会议的主题和会议时长是否符合预期。

    参数:
        expected_topic (str): 期望的会议主题。
        expected_duration_minutes (int): 期望的会议时长（单位：分钟）。
        duration_tolerance_minutes (int, optional): 会议时长的容差（单位：分钟）。Defaults to 5。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果最近一场已结束会议的主题和时长都符合预期，返回True，否则返回False。
    """

    # 使用常量
    expected_topic = EXPECTED_TOPIC
    expected_duration_minutes = EXPECTED_DURATION_MINUTES
    duration_tolerance_minutes = DEFAULT_DURATION_TOLERANCE_MINUTES

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_13")

    data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETINGS_FILE}",
        backup_dir=backup_dir,
    )

    if data is None:
        logging.error(f"错误: 无法从设备读取或解析 {MEETINGS_FILE}。")
        return False

    try:
        ended_meetings_with_time = [
            m
            for m in data
            if m.get(MEETING_STATUS_KEY) == MEETING_STATUS_ENDED
            and m.get(MEETING_END_TIME_KEY) is not None
            and m.get(MEETING_START_TIME_KEY) is not None
        ]

        if not ended_meetings_with_time:
            logging.error("错误: 未找到任何已结束的会议。")
            return False

        recent_meeting = max(ended_meetings_with_time, key=lambda x: x.get(MEETING_END_TIME_KEY, 0))

        actual_topic = recent_meeting.get(MEETING_TOPIC_KEY)
        start_time_ms = recent_meeting.get(MEETING_START_TIME_KEY, 0)
        end_time_ms = recent_meeting.get(MEETING_END_TIME_KEY, 0)

        actual_duration_ms = end_time_ms - start_time_ms
        actual_duration_minutes = round(actual_duration_ms / (1000 * 60))

        # 检查主题是否匹配
        topic_match = actual_topic == expected_topic

        # 检查时长是否在容差范围内
        duration_match = abs(actual_duration_minutes - expected_duration_minutes) <= duration_tolerance_minutes

        if not (topic_match and duration_match):
            logging.error(
                "Latest ended meeting details mismatch: topic=%r expected_topic=%r duration=%s expected_duration=%s tolerance=%s.",
                actual_topic,
                expected_topic,
                actual_duration_minutes,
                expected_duration_minutes,
                duration_tolerance_minutes,
            )
            return False

        details_evidence = [
            actual_topic,
            recent_meeting.get("meetingId"),
            end_time_ms,
        ]
        return answer_contains_any(result, details_evidence) or answer_contains_number(result, actual_duration_minutes)


    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False

if __name__ == '__main__':
    print(get_latest_ended_meeting_details())
