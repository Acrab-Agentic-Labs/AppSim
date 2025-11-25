import json
import subprocess
import os

# 任务26：选上海的酒店，入住日期选10月22日，退房10月25日，客房数和入住人数默认，得到酒店列表后，点击第一个酒店，然后选择第一个房型预订
# 检查条件：type="hotel_booking", city="上海", checkIn="2025-10-22", checkOut="2025-10-25", hotelIndex=0, roomIndex=0


def check_booking_hotel_shanghai(result=None, device_id=None, backup_dir=None):
    app_package = "com.example.Ctrip"
    phone_file_path = "files/booking_history.json"
    local_file_path = os.path.join(backup_dir, 'booking_history.json') if backup_dir else 'booking_history.json'

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

    # 3. 检查最新预订记录是否包含指定字段
    try:
        booking_events = data.get("booking_events", [])
        if not booking_events:
            return False
        latest_event = booking_events[-1]
        return (
            latest_event.get("type") == "hotel_booking"
            and latest_event.get("city") == "上海"
            and latest_event.get("checkIn") == "2025-10-22"
            and latest_event.get("checkOut") == "2025-10-25"
            and latest_event.get("hotelIndex") == 0
            and latest_event.get("roomIndex") == 0
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if check_booking_hotel_shanghai() else "false")
