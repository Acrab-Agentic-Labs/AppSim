import json
import logging
import os
import pathlib
import subprocess
import time


def run_app_with_clear_data(
    app_package: str = "com.example.myele",  # App包名（你的目标包名）
    main_activity: str = ".MainActivity",  # 主Activity路径
    device_id: str = "122.228.230.212:10209",  # 目标设备ID（从你的日志中获取）
) -> bool:
    # ---------------------- 第一步：清除App数据（指定设备） ----------------------
    logging.info(f"[1/2] 正在清除 {app_package} 的数据（设备：{device_id}）...")
    clear_result = subprocess.run(
        ["adb", "-s", device_id, "shell", "pm", "clear", app_package],  # 关键：添加 -s device_id
        capture_output=True,
        text=True,
        encoding="utf-8",  # 避免中文乱码
    )
    if clear_result.stdout.strip() != "Success":
        logging.error(f"❌ 清除数据失败！错误信息：{clear_result.stderr.strip() or clear_result.stdout.strip()}")
        return False
    logging.info("✅ 数据清除成功")

    # ---------------------- 第2步：启动主Activity（指定设备） ----------------------
    logging.info(f"[2/2] 正在启动 {app_package}/{main_activity}（设备：{device_id}）...")
    start_result = subprocess.run(
        [
            "adb",
            "-s",
            device_id,
            "shell",
            "am",
            "start",
            "-n",
            f"{app_package}/{main_activity}",
        ],  # 同样添加 -s device_id
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    # 检查启动是否成功（输出包含"Starting: Intent"且无明显错误）
    if "Starting: Intent" in start_result.stdout and "Error" not in start_result.stderr:
        logging.info("✅ App启动成功！")
        time.sleep(5)
        return True
    else:
        logging.error(f"❌ 启动Activity失败！错误信息：{start_result.stderr.strip() or start_result.stdout.strip()}")
        return False


def read_jsonl(file_path: str) -> list:
    import json

    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def write_jsonl(file_path, list_of_dicts):
    import json

    with open(file_path, "w", encoding="utf-8") as f:
        for item in list_of_dicts:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def pull_file_from_device(device_id: str, package_name: str, device_file_path: str, local_file_path: str) -> str:
    """从设备拉取文件到本地

    参数:
        device_id: 设备ID
        package_name: 包名
        device_file_path: 设备文件路径
        local_file_path: 本地文件路径

    返回:
        local_file_path: 本地文件路径

    Raise:
        FileNotFoundError: 文件不存在
    """

    # 检查文件是否存在
    _NO_FILE_STR = "No such file or directory"
    cmd = ["adb", "-s", device_id, "exec-out", "run-as", package_name, "ls", device_file_path]
    result = subprocess.run(cmd, encoding="utf-8", capture_output=True)
    if _NO_FILE_STR in result.stdout:
        raise FileNotFoundError(f"File not found: {device_id}:{package_name}:{device_file_path}")

    # 拉取文件
    cmd = ["adb", "-s", device_id, "exec-out", "run-as", package_name, "cat", device_file_path]
    with open(local_file_path, "w", encoding="utf-8") as fw:
        subprocess.run(cmd, stdout=fw)


def read_json_from_device(device_id: str, package_name: str, device_json_path: str, backup_dir: str) -> dict:
    """从设备读取JSON文件

    参数:
        device_id: 设备ID
        package_name: 包名
        device_json_path: 设备上的JSON文件路径(相对于app私有目录)
        backup_dir: 备份目录

    返回:
        JSON数据

    Raise:
        FileNotFoundError: 文件不存在
    """
    pathlib.Path(backup_dir).mkdir(parents=True, exist_ok=True)

    local_file_path = os.path.join(backup_dir, pathlib.Path(device_json_path).name)
    pull_file_from_device(device_id, package_name, device_json_path, local_file_path)

    # 读取JSON
    with open(local_file_path, "r", encoding="utf-8") as fr:
        data = json.load(fr)

    return data
