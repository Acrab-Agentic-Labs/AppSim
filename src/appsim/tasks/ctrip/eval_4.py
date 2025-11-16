import subprocess
import json

# 任务4：点击"消息"按钮
# 检查条件：icon="消息", page="消息页面"


def check_click_message(result=None, device_id=None):
    app_package = "com.example.Ctrip"
    phone_file_path = "files/click_history.json"

    # 1. 通过ADB获取文件内容（指定编码为UTF-8，避免解码错误）
    try:
        # 构建adb命令，如果提供了device_id就添加设备选择参数
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", phone_file_path])

        # 使用stdout=subprocess.PIPE，配合universal_newlines和encoding参数处理编码
        result1 = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # 启用文本模式
            encoding="utf-8",  # 强制指定UTF-8编码解析输出
            check=True,
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

    # 3. 检查最新记录
    try:
        latest_event = data["click_events"][-1]
        return latest_event["icon"] == "消息" and latest_event["page"] == "消息页面"
    except:
        return False


if __name__ == "__main__":
    print("true" if check_click_message() else "false")
