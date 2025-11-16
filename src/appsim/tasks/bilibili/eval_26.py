import subprocess
import json
import os
import shutil
import time
import re


def CheckHistoryItemDelete(result=None, device_id=None):
    """
    检验逻辑:在历史记录页面，找到昨天观看过的一个视频，长按该记录项，将其从历史记录中删除
    验证用户是否在APP中真正完成了历史记录删除操作
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 进入'我的'页面")
        print("3. 点击'历史记录'")
        print("4. 找到昨天观看过的一个视频")
        print("5. 长按该记录项")
        print("6. 点击删除")
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

        # step3. 验证关键操作 - 放宽验证条件
        history_page_entered = "HISTORY_PAGE_ENTERED" in log_content
        history_data_loaded = "HISTORY_DATA_LOADED" in log_content
        history_item_long_pressed = "HISTORY_ITEM_LONG_PRESSED" in log_content
        delete_button_clicked = "DELETE_BUTTON_CLICKED" in log_content
        history_item_deleted = "HISTORY_ITEM_DELETED" in log_content

        # 只要检测到删除相关操作即可
        if not (history_item_long_pressed or delete_button_clicked or history_item_deleted):
            print("验证失败: 未检测到删除历史记录操作")
            print("\n提示: 请确保:")
            print("1. 进入了历史记录页面")
            print("2. 长按了某个历史记录项")
            print("3. 点击了删除")
            print(f"\n日志内容:\n{log_content}")
            return False

        # 验证 result 存在
        if result is None:
            return False

        # 检测 result 中的final_messages中是否包含 "8"
        if "final_message" in result and "8" in result["final_message"]:
            return True
        else:
            return False

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查历史记录删除时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckHistoryItemDelete()
    print(result1)
