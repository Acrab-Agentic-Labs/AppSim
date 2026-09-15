import json
import subprocess
import os

# 任务30：进入"火车票"页面，选出发地"北京"、目的地"上海"，选择日期10月20日，得到车次列表后，预订下午1点到下午3点的任意一班车次
# 检查条件：type="train_booking", from="北京", to="上海", date="2025-10-20", departureTime在13:00-15:00范围内


def verify_train_booking_for_requested_time(result=None, device_id=None, backup_dir=None):
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

    # 3. 检查最新预订记录是否包含指定字段
    try:
        booking_events = data.get("booking_events", [])
        if not booking_events:
            return False
        latest_event = booking_events[-1]

        # 检查基本字段
        if (
            latest_event.get("type") != "train_booking"
            or latest_event.get("from") != "北京"
            or latest_event.get("to") != "上海"
            or latest_event.get("date") != "2025-10-20"
        ):
            return False

        # 检查departureTime是否在13:00-15:00范围内
        departure_time = latest_event.get("departureTime", "")
        if not departure_time:
            return False

        # 解析时间 "HH:MM"
        time_parts = departure_time.split(":")
        if len(time_parts) != 2:
            return False

        try:
            hour = int(time_parts[0])
            minute = int(time_parts[1])

            # 转换为分钟数进行比较
            total_minutes = hour * 60 + minute

            # 13:00 = 780分钟, 15:00 = 900分钟
            # 判断是否在13:00到15:00之间（不包括15:00）
            return 780 <= total_minutes < 900
        except ValueError:
            return False

    except:
        return False


if __name__ == "__main__":
    print("true" if verify_train_booking_for_requested_time() else "false")
