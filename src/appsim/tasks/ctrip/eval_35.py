import subprocess
import json

# 任务35：订10月25日北京飞上海的6张经济舱机票
# 检查条件：最后6条记录都是：机票(北京->上海, 2025-10-25, 经济舱)


def check_booking_batch_flight(result=None, device_id=None):
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

    # 3. 检查最后6条预订记录
    try:
        booking_events = data.get("booking_events", [])
        if len(booking_events) < 6:
            return False

        # 获取最后6条记录
        last_six = booking_events[-6:]

        # 验证所有6条记录都是机票(北京->上海, 2025-10-25, 经济舱)
        for record in last_six:
            if not (
                record.get("type") == "flight_booking"
                and record.get("from") == "北京"
                and record.get("to") == "上海"
                and record.get("date") == "2025-10-25"
                and record.get("cabin") == "经济舱"
            ):
                return False

        return True
    except:
        return False


if __name__ == "__main__":
    print("true" if check_booking_batch_flight() else "false")
