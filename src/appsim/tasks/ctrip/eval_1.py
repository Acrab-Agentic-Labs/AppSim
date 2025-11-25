import json
import subprocess
import os


def check_click_hotel(result=None, device_id=None, backup_dir=None):
    app_package = "com.example.Ctrip"
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
        return latest_event["icon"] == "酒店" and latest_event["page"] == "酒店预订页面"
    except:
        return False


if __name__ == "__main__":
    print(check_click_hotel())
