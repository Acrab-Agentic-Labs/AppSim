import json
import subprocess
import os

# 任务9：进入"酒店"页面，选择房间1间、成人1位、儿童1位，得到酒店列表
# 检查条件：type="hotel_search", rooms=1, adults=1, children=1


def check_hotel_search_guests(result=None, device_id=None, backup_dir=None):
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

    # 3. 检查最新记录是否包含指定字段且显示了列表
    try:
        latest_event = data["search_events"][-1]
        return (
            latest_event.get("type") == "hotel_search"
            and latest_event.get("rooms") == 1
            and latest_event.get("adults") == 1
            and latest_event.get("children") == 1
            and latest_event.get("list_shown") == True
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if check_hotel_search_guests() else "false")
