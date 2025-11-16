import subprocess
import json
import os
import shutil
import time


def CheckSearchGame(result=None, device_id=None):
    """
    检验逻辑:在首页搜索框输入游戏解说，点击搜索按钮
    验证用户是否完成搜索操作
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 在首页搜索框输入'游戏解说'")
        print("3. 点击搜索按钮")
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

        # step3. 验证是否输入了搜索内容
        if "SEARCH_INPUT" not in log_content or "游戏解说" not in log_content:
            print("验证失败: 未检测到输入'游戏解说'")
            print(f"日志内容:\n{log_content}")
            return False

        # step4. 验证是否点击了搜索按钮
        if "SEARCH_BUTTON_CLICKED" not in log_content:
            print("验证失败: 未检测到点击搜索按钮")
            print(f"日志内容:\n{log_content}")
            return False

        # step5. 验证是否成功跳转到游戏搜索结果页面
        if "GAME_SEARCH_PAGE_LOADED" not in log_content:
            print("验证失败: 未成功跳转到游戏搜索结果页面")
            print(f"日志内容:\n{log_content}")
            return False

        print("搜索操作验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查搜索操作时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckSearchGame()
    print(result1)
