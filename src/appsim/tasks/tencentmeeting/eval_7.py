"""
功能: 验证未开始会议的数目
验证目标: 检查status为UPCOMING的会议数量
数据来源: meetings.json
"""

import os
import logging

try:
    from ._answer_utils import answer_contains_any, answer_contains_number
except ImportError:
    from _answer_utils import answer_contains_any, answer_contains_number


# ============================================================================
# 常量定义 - 每个脚本独立定义
# ============================================================================

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
EXPECTED_COUNT = 16

# 数据文件常量
MEETINGS_FILE = "meetings.json"
USERS_FILE = "users.json"
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
PERSONAL_MEETING_ROOMS_FILE = "personal_meeting_rooms.json"
MESSAGES_FILE = "messages.json"
HAND_RAISE_RECORDS_FILE = "hand_raise_records.json"
MEETING_INVITATIONS_FILE = "meeting_invitations.json"

# JSON字段名常量
MEETING_ID_KEY = "meetingId"
USER_ID_KEY = "userId"
MEETING_STATUS_KEY = "status"
MEETING_TYPE_KEY = "meetingType"
PARTICIPANT_IDS_KEY = "participantIds"
IS_MUTED_KEY = "isMuted"
IS_CAMERA_ON_KEY = "isCameraOn"
IS_SHARING_SCREEN_KEY = "isSharingScreen"
IS_HAND_RAISED_KEY = "isHandRaised"

# 业务常量
MEETING_STATUS_UPCOMING = "UPCOMING"
MEETING_STATUS_ONGOING = "ONGOING"
MEETING_STATUS_ENDED = "ENDED"
MEETING_TYPE_INSTANT = "INSTANT"
MEETING_TYPE_SCHEDULED = "SCHEDULED"
MEETING_TYPE_PERSONAL = "PERSONAL"


# ============================================================================
# 工具函数 - read_json_from_device 内联实现
# ============================================================================

def read_json_from_device(
    device_id: str,
    package_name: str,
    device_json_path: str,
    backup_dir: str
) -> dict or list or None:
    """
    从Android设备读取JSON文件并返回解析后的数据。

    此函数是appsim.utils.read_json_from_device的独立实现，
    确保每个脚本完全自包含，无外部依赖。

    参数:
        device_id (str): Android设备ID（adb设备序列号）
        package_name (str): 应用包名
        device_json_path (str): 设备上JSON文件的相对路径（相对于app私有目录）
        backup_dir (str): 本地备份目录路径

    返回:
        dict/list/None: 解析后的JSON数据，失败返回None
    """
    import subprocess
    import pathlib
    import json

    # 创建备份目录
    pathlib.Path(backup_dir).mkdir(parents=True, exist_ok=True)

    # 本地文件路径
    local_file_path = os.path.join(backup_dir, pathlib.Path(device_json_path).name)

    try:
        # 检查设备文件是否存在
        _NO_FILE_STR = "No such file or directory"
        cmd_ls = ["adb", "-s", device_id, "exec-out", "run-as", package_name, "ls", device_json_path]
        result_ls = subprocess.run(cmd_ls, encoding="utf-8", capture_output=True, check=False)

        if _NO_FILE_STR in result_ls.stdout or result_ls.returncode != 0:
            logging.error(
                f"文件在设备上不存在: {device_id}:{package_name}:{device_json_path}. "
                f"Stderr: {result_ls.stderr.strip()}"
            )
            raise FileNotFoundError(
                f"File not found: {device_id}:{package_name}:{device_json_path}"
            )

        # 拉取文件
        cmd_cat = ["adb", "-s", device_id, "exec-out", "run-as", package_name, "cat", device_json_path]
        with open(local_file_path, "w", encoding="utf-8") as fw:
            result_cat = subprocess.run(cmd_cat, stdout=fw, stderr=subprocess.PIPE, check=False)

        if result_cat.returncode != 0:
            logging.error(f"ADB cat命令执行失败: {device_json_path}. Stderr: {result_cat.stderr.strip()}")
            raise Exception(f"ADB cat command failed for {device_json_path}")

        # 解析JSON
        with open(local_file_path, "r", encoding="utf-8") as fr:
            data = json.load(fr)

        logging.info(f"成功从设备读取JSON: {device_json_path}")
        return data

    except FileNotFoundError:
        logging.error(f"设备文件不存在: {device_json_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"JSON解析失败: {local_file_path}, 错误: {e}")
        return None
    except Exception as e:
        logging.error(f"读取设备JSON文件时发生未知错误: {e}")
        return None


# ============================================================================
# 验证函数 - 核心业务逻辑
# ============================================================================

def verify_not_started_meeting_count(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证未开始会议的数目是否与预期匹配。

    参数:
        expected_count (int): 期望的未开始会议数目。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。如果为 None，则默认路径为
                                     os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_reasoning_tasks")。

    返回:
        bool: 如果实际未开始会议数目与期望数目匹配则返回True，否则返回False。
    """

    # 使用常量
    expected_count = EXPECTED_COUNT

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_34")

    meetings_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETINGS_FILE}",
        backup_dir=backup_dir,
    )

    if meetings_data is None:
        print(f"错误: 无法从设备读取或解析 {MEETINGS_FILE}。")
        return False

    actual_count = len([m for m in meetings_data if m.get(MEETING_STATUS_KEY) == "UPCOMING"])
    if actual_count != expected_count:
        logging.error("Upcoming meeting count %s did not match expected %s.", actual_count, expected_count)
        return False

    return answer_contains_number(result, actual_count)


if __name__ == '__main__':
    print(read_json_from_device())
