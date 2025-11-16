import subprocess
import json

# 任务31：先订北京飞上海的机票（10月20日，经济舱），再订上海的酒店（入住10月20日，退房10月21日），最后订上海回北京的火车票（10月21日）
# 检查条件：最后3条记录依次是：机票(北京->上海)、酒店(上海)、火车票(上海->北京)


def check_booking_multi_step(result=None, device_id=None):
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

    # 3. 检查最后3条预订记录
    try:
        booking_events = data.get("booking_events", [])
        if len(booking_events) < 3:
            return False

        # 获取最后3条记录
        last_three = booking_events[-3:]

        # 验证第1步：机票(北京->上海)
        step1 = last_three[0]
        if not (step1.get("type") == "flight_booking" and step1.get("from") == "北京" and step1.get("to") == "上海"):
            return False

        # 验证第2步：酒店(上海)
        step2 = last_three[1]
        if not (step2.get("type") == "hotel_booking" and step2.get("city") == "上海"):
            return False

        # 验证第3步：火车票(上海->北京)
        step3 = last_three[2]
        if not (step3.get("type") == "train_booking" and step3.get("from") == "上海" and step3.get("to") == "北京"):
            return False

        return True
    except:
        return False


if __name__ == "__main__":
    print("true" if check_booking_multi_step() else "false")
