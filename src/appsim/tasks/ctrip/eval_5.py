import json
import subprocess
import os

# 任务5：点击"行程"按钮
# 检查条件：icon="行程", page="行程页面"


def verify_itinerary_page_opened(result=None, device_id=None, backup_dir=None):
    app_package = "com.example.ctrip_sim"
    phone_file_path = "files/click_history.json"
    local_file_path = os.path.join(backup_dir, 'click_history.json') if backup_dir else 'click_history.json'

    # 1. 通过ADB获取文件内容
    try:
        # 构建adb命令，如果提供了device_id就添加设备选择参数
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", phone_file_path])

        with open(local_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f)

        # 2. 解析JSON内容
        with open(local_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False

    # 3. 检查最新记录
    try:
        latest_event = data["click_events"][-1]
        return latest_event["icon"] == "行程" and latest_event["page"] == "行程页面"
    except:
        return False


if __name__ == "__main__":
    print("true" if verify_itinerary_page_opened() else "false")
