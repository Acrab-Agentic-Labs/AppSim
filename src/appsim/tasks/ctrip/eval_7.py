import json
import subprocess
import os

# 任务7：酒店搜索上海
# 检查条件：type="hotel_search", city="上海"


def check_hotel_search_chengdu(result=None, device_id=None, backup_dir=None):
    app_package = "com.example.ctrip_sim"
    phone_file_path = "files/search_params.json"
    local_file_path = os.path.join(backup_dir, 'search_params.json') if backup_dir else 'search_params.json'

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

    # 3. 检查最新记录是否符合条件且显示了列表
    try:
        latest_event = data["search_events"][-1]
        return (
            latest_event.get("type") == "hotel_search"
            and latest_event.get("city") == "上海"
            and latest_event.get("list_shown") == True
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if check_hotel_search_chengdu() else "false")
