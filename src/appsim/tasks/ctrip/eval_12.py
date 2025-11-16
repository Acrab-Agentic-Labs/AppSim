import subprocess
import json

# 任务12：进入"机票"页面，选择公务/头等舱，得到航班列表
# 检查条件：type="flight_search", cabin字段为"公务/头等舱"


def check_flight_search_cabin(result=None, device_id=None):
    app_package = "com.example.Ctrip"
    phone_file_path = "files/search_params.json"

    # 1. 通过ADB获取文件内容
    try:
        # 构建adb命令，如果提供了device_id就添加设备选择参数
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

    # 3. 检查最新记录是否包含指定字段且显示了列表
    try:
        latest_event = data["search_events"][-1]
        return (
            latest_event.get("type") == "flight_search"
            and latest_event.get("cabin") == "公务/头等舱"
            and latest_event.get("list_shown") == True
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if check_flight_search_cabin() else "false")
