import json
import subprocess
import os

# 任务10：进入"机票"页面，选择出发地"广州"、目的地"深圳"，得到航班列表
# 检查条件：type="flight_search", from="广州", to="深圳"


def verify_flight_search_results_for_requested_route(result=None, device_id=None, backup_dir=None):
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
            latest_event.get("type") == "flight_search"
            and latest_event.get("from") == "广州"
            and latest_event.get("to") == "深圳"
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if verify_flight_search_results_for_requested_route() else "false")
