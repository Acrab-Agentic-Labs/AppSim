import json
import re
import subprocess

# 任务33：订5张10月20日深圳到北京的火车票（要求5小时内到达）
# 检查条件：最后5条记录都是：火车票(深圳->北京, 2025-10-20, duration<=5小时)


def parse_duration(duration_str):
    """
    解析时长字符串，如 "4时55分" -> 295分钟
    """
    hour_match = re.search(r"(\d+)时", duration_str)
    minute_match = re.search(r"(\d+)分", duration_str)

    hours = int(hour_match.group(1)) if hour_match else 0
    minutes = int(minute_match.group(1)) if minute_match else 0

    return hours * 60 + minutes


def check_booking_batch_train(result=None, device_id=None):
    app_package = "com.example.Ctrip"
    phone_file_path = "files/booking_history.json"

    # 1. 通过ADB获取文件内容
    try:
        # 构建adb命令,如果提供了device_id就添加设备选择参数
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", phone_file_path])

        result1 = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8", check=True
        )
        file_content = result1.stdout
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False

    # 2. 解析JSON内容
    try:
        data = json.loads(file_content)
    except json.JSONDecodeError:
        return False
    except Exception:
        return False

    # 3. 检查最后5条预订记录
    try:
        booking_events = data.get("booking_events", [])
        if len(booking_events) < 5:
            return False

        # 获取最后5条记录
        last_five = booking_events[-5:]

        # 验证所有5条记录都是火车票(深圳->北京, 2025-10-20)，且5小时内到达
        for record in last_five:
            if not (
                record.get("type") == "train_booking"
                and record.get("from") == "深圳"
                and record.get("to") == "北京"
                and record.get("date") == "2025-10-20"
            ):
                return False

            # 检查时长是否5小时内
            duration = record.get("duration", "")
            if duration:
                duration_minutes = parse_duration(duration)
                if duration_minutes > 300:  # 5小时 = 300分钟
                    return False
            else:
                return False  # 没有时长信息，返回false

        return True
    except:
        return False


if __name__ == "__main__":
    print("true" if check_booking_batch_train() else "false")
