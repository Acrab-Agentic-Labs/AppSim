import json
import subprocess
import os

# 任务34：订5张10月20日广州到北京的火车票，再订北京3家不同的酒店
# 检查条件：最后8条记录前5条是火车票(广州->北京, 2025-10-20)，后3条是酒店(北京,不同酒店)


def check_booking_complex_batch(result=None, device_id=None, backup_dir=None):
    app_package = "com.example.ctrip_sim"
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

    # 3. 检查最后8条预订记录
    try:
        booking_events = data.get("booking_events", [])
        if len(booking_events) < 8:
            return False

        # 获取最后8条记录
        last_eight = booking_events[-8:]

        # 验证前5条记录都是火车票(广州->北京, 2025-10-20)
        for i in range(5):
            record = last_eight[i]
            if not (
                record.get("type") == "train_booking"
                and record.get("from") == "广州"
                and record.get("to") == "北京"
                and record.get("date") == "2025-10-20"
            ):
                return False

        # 验证后3条记录都是酒店(北京)
        hotel_names = []
        for i in range(5, 8):
            record = last_eight[i]
            if not (record.get("type") == "hotel_booking" and record.get("city") == "北京"):
                return False

            # 收集酒店名称以检查是否不同
            hotel_name = record.get("hotelName", "")
            hotel_names.append(hotel_name)

        # 验证3家酒店的名称都不同
        if len(set(hotel_names)) != 3:
            return False

        return True
    except:
        return False


if __name__ == "__main__":
    print("true" if check_booking_complex_batch() else "false")
