import logging
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
