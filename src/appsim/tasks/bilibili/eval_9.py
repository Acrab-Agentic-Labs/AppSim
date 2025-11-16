import subprocess
import json
import os
import shutil
import time


def CheckProfilePage(result=None, device_id=None):
    """
    检验逻辑:在我的页面，点击顶部头像或昵称区域，进入个人资料页查看信息
    验证用户是否进入个人资料页
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 点击底部'我的'页面")
        print("3. 点击顶部头像或昵称区域")
        print("4. 进入个人资料页查看信息")
        print("=" * 60)

        # step2. 读取logcat日志
        print("\n正在检查日志...")
        cmd_logcat = ["adb"]
        if device_id:
            cmd_logcat.extend(["-s", device_id])
        cmd_logcat.extend(["logcat", "-d", "-s", "BilibiliAutoTest:D"])

        result1 = subprocess.run(
            cmd_logcat,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="ignore",  # 忽略无法解码的字符
        )

        log_content = result1.stdout

        # step3. 验证关键操作 - 只需要检测到PersonTab即可
        person_tab_detected = "PersonTab" in log_content

        if not person_tab_detected:
            print("验证失败: 未检测到PersonTab")
            print("\n提示: 请确保:")
            print("1. 在我的页面点击了顶部头像或昵称")
            print("2. 已进入个人资料页")
            print(f"\n日志内容:\n{log_content}")
            return False

        # 验证 result 存在
        if result is None:
            return False

        # 检测 result 中的final_messages中是否包含 "凡人修仙传"
        if "final_message" in result and "凡人修仙传" in result["final_message"]:
            return True
        else:
            return False

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查个人资料页时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckProfilePage()
    print(result1)
