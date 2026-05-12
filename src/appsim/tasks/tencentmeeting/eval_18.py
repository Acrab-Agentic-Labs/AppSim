"""
功能: 计算所有已结束会议的平均时长
数据库位置: meetings.json
"""

import os
import logging
from appsim.utils import read_json_from_device
try:
    from ._answer_utils import answer_contains_any, answer_contains_number
except ImportError:
    from _answer_utils import answer_contains_any, answer_contains_number


PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
EXPECTED_MINUTES = 78
TOLERANCE = 5
MEETINGS_FILE = "meetings.json"

def verify_average_meeting_duration(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证所有已结束会议的平均时长。

    参数:
        expected_minutes (int): 期望的平均时长（分钟）。
        tolerance (int): 容差范围（分钟）。默认为5分钟。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_33")。

    返回:
        bool: 如果实际平均时长在期望范围内则返回True，否则返回False。
    """

    # 使用常量
    expected_minutes = EXPECTED_MINUTES
    tolerance = TOLERANCE

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_33")

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
        # 过滤已结束的会议
        ended_meetings = [m for m in meetings_data if m.get("status") == "ENDED"]

        if not ended_meetings:
            logging.error("没有找到已结束的会议。")
            return False

        # 计算每个会议的时长（分钟）
        durations = []
        MAX_REASONABLE_DURATION_MINUTES = 24 * 60  # 24小时
        for meeting in ended_meetings:
            start_time = meeting.get("startTime")
            end_time = meeting.get("endTime")

            if start_time and end_time:
                duration_minutes = (end_time - start_time) / (1000 * 60)
                # 过滤掉不合理的时长（负数或超过24小时）
                if 0 < duration_minutes <= MAX_REASONABLE_DURATION_MINUTES:
                    durations.append(duration_minutes)
                else:
                    logging.warning(f"跳过不合理的会议时长: {duration_minutes:.1f} 分钟 (会议ID: {meeting.get('meetingId', 'unknown')})")

        if not durations:
            logging.error("没有找到有效的会议时长数据。")
            return False

        # 计算平均时长
        avg_duration = sum(durations) / len(durations)

        # 检查是否在容差范围内
        if abs(avg_duration - expected_minutes) > tolerance:
            logging.error(
                "Average ended-meeting duration was %.1f minutes, expected %s within tolerance %s.",
                avg_duration,
                expected_minutes,
                tolerance,
            )
            return False

        return answer_contains_number(result, round(avg_duration)) or answer_contains_number(result, round(avg_duration, 1))
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    import shutil
    temp_backup_dir = os.path.join(os.getcwd(), "temp_eval_backup_33")

    print("注意: 本地测试无法模拟真实设备文件拉取。")
    print(f"假设调用: verify_average_meeting_duration(expected_minutes=88, tolerance=5, backup_dir='{temp_backup_dir}')")

    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)


if __name__ == '__main__':
    print(verify_average_meeting_duration())
