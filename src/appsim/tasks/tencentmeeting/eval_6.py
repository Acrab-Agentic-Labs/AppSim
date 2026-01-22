"""
功能: 通过手机号搜索联系人
验证目标: 检查是否能通过手机号搜索到特定用户
数据来源: users.json
"""

import os
import logging

# ============================================================================
# 常量定义 - 每个脚本独立定义
# ============================================================================

PACKAGE_NAME = "com.example.tencent_meeting_sim"

# 任务特定常量
EXPECTED_PHONE_NUMBER = "15823467912"
DATA_FILE = "users.json"

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

def check_search_user_by_phone(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    检查是否能通过手机号搜索到特定用户。

    参数:
        expected_phone_number (str): 期望找到的手机号码。
        device_id (str, optional): Android设备的ID. Defaults to None.
        backup_dir (str, optional): 备份文件存放的目录。

    返回:
        bool: 如果找到的用户手机号匹配期望值则返回True, 否则返回False。
    """

    # 使用常量
    expected_phone_number = EXPECTED_PHONE_NUMBER

    if backup_dir is None:
        backup_dir = os.path.join(os.getcwd(), "scripts_backup", "tencentmeeting_eval_13")

    data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{DATA_FILE}",
        backup_dir=backup_dir,
    )

    if data is None:
        logging.error(f"错误: 无法从设备读取或解析 {DATA_FILE}。")
        return False

    try:
        for user in data:
            if user.get("phone") == expected_phone_number:
                return True

        logging.error(f"未找到手机号为 {expected_phone_number} 的用户。")
        return False
    except Exception as e:
        logging.error(f"处理数据时发生错误: {e}")
        return False


if __name__ == '__main__':
    print(read_json_from_device())
