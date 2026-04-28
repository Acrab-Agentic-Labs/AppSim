import json
import os
import subprocess

# 任务21：进入"火车票"页面，选择出发地"杭州"、目的地"深圳"、选择日期10月24日，选择学生票，得到车次列表
# 检查条件：type="train_search", from="杭州", to="深圳", date="2025-10-24", ticketType="学生票"


def check_train_search_hz_sz_student(result=None, device_id=None, backup_dir=None):
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
            latest_event.get("type") == "train_search"
            and latest_event.get("from") == "杭州"
            and latest_event.get("to") == "深圳"
            and latest_event.get("date") == "2025-10-24"
            and latest_event.get("ticketType") == "学生票"
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if check_train_search_hz_sz_student() else "false")
