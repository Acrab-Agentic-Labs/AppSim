import json
import os
import subprocess

# 任务17：进入"酒店"页面，城市选上海，入住时间今天、退房时间明天，房间选择2间、成人选择2位、儿童选择0位，得到酒店列表
# 检查条件：type="hotel_search", city="上海", checkIn="2025-10-20", checkOut="2025-10-21", rooms=2, adults=2, children=0


def verify_hotel_search_results_for_guest_counts_and_dates(result=None, device_id=None, backup_dir=None):
    app_package = "com.example.ctrip_sim"
    phone_file_path = "files/search_params.json"
    local_file_path = os.path.join(backup_dir, 'search_params.json') if backup_dir else 'search_params.json'

    # 1. 通过ADB获取文件内容
    try:
        # 构建adb命令,如果提供了device_id就添加设备选择参数
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
            and latest_event.get("city") == "上海"
            and latest_event.get("checkIn") == "2025-10-20"
            and latest_event.get("checkOut") == "2025-10-21"
            and latest_event.get("rooms") == 2
            and latest_event.get("adults") == 2
            and latest_event.get("children") == 0
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if verify_hotel_search_results_for_guest_counts_and_dates() else "false")
