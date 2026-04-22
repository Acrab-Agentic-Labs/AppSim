import json
import subprocess
import os


def check_click_flight(result=None, device_id=None, backup_dir=None):
    """
    任务2: 点击 "机票" 图标，进入机票预订界面
    检验方法: 维护点击记录存储
    """
    # 定义APP包名和存储点击记录的文件路径
    app_package = "com.example.ctrip_sim"
    phone_file_path = "files/click_history.json"
    local_file_path = os.path.join(backup_dir, 'click_history.json') if backup_dir else 'click_history.json'

    try:
        # 1. 通过ADB获取文件内容
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", phone_file_path])

        with open(local_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f)

        # 2. 解析JSON内容
        with open(local_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 3. 检查最新记录
        latest_event = data["click_events"][-1]
        return latest_event["icon"] == "机票" and latest_event["page"] == "机票预订页面"
    except:
        return False


if __name__ == "__main__":
    result1 = check_click_flight()
    print("true" if result1 else "false")
