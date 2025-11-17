import json
import subprocess

# 任务27：进入"机票"页面，选出发地"成都"、目的地"深圳"，选择日期10月24号，舱型默认，得到航班列表后，预订第一架航班
# 检查条件：type="flight_booking", from="成都", to="深圳", date="2025-10-24", flightIndex=0


def check_booking_flight_wh_sz(result=None, device_id=None):
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

    # 3. 检查最新预订记录是否包含指定字段
    try:
        booking_events = data.get("booking_events", [])
        if not booking_events:
            return False
        latest_event = booking_events[-1]
        return (
            latest_event.get("type") == "flight_booking"
            and latest_event.get("from") == "成都"
            and latest_event.get("to") == "深圳"
            and latest_event.get("date") == "2025-10-24"
            and latest_event.get("flightIndex") == 0
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if check_booking_flight_wh_sz() else "false")
