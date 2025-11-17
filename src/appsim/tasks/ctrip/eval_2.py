import json
import subprocess


def check_click_flight(result=None, device_id=None):
    """
    任务2: 点击 "机票" 图标，进入机票预订界面
    检验方法: 维护点击记录存储
    """
    # 定义APP包名和存储点击记录的文件路径
    app_package = "com.example.Ctrip"
    file_path = "files/click_history.json"

    # 1. 通过ADB直接读取文件内容
    try:
        # 构建adb命令，如果提供了device_id就添加设备选择参数
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", file_path])

        result1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", check=True)
        file_content = result1.stdout
    except subprocess.CalledProcessError:
        print("获取文件失败，可能文件不存在或权限不足")
        return False

    # 2. 解析JSON内容
    try:
        data = json.loads(file_content)
    except json.JSONDecodeError:
        print("文件解析失败")
        return False

    # 3. 检查最新记录
    try:
        latest_event = data["click_events"][-1]
        return latest_event["icon"] == "机票" and latest_event["page"] == "机票预订页面"
    except:
        return False


if __name__ == "__main__":
    result1 = check_click_flight()
    print("true" if result1 else "false")
