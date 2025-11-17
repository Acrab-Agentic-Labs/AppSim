import json
import subprocess

# 任务7：酒店搜索上海
# 检查条件：type="hotel_search", city="上海"


def check_hotel_search_chengdu(result=None, device_id=None):
    app_package = "com.example.Ctrip"
    phone_file_path = "files/search_params.json"

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

    # 3. 检查最新记录是否符合条件且显示了列表
    try:
        latest_event = data["search_events"][-1]
        return (
            latest_event.get("type") == "hotel_search"
            and latest_event.get("city") == "上海"
            and latest_event.get("list_shown") == True
        )
    except:
        return False


if __name__ == "__main__":
    print("true" if check_hotel_search_chengdu() else "false")
