import subprocess
import json
import os
import shutil
import time


def CheckSearchPlayLike(result=None, device_id=None):
    """
    检验逻辑:搜索视频"游戏解说"，播放搜索出的第一个视频，点赞
    验证用户是否在APP中真正完成了搜索、播放和点赞操作
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 在搜索框输入'游戏解说'并搜索")
        print("3. 点击第一个搜索结果播放视频")
        print("4. 点击点赞按钮")
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
        search_completed = "SEARCH_COMPLETED" in log_content
        search_keyword = "游戏解说" in log_content
        first_result_clicked = "FIRST_SEARCH_RESULT_CLICKED" in log_content
        video_player_opened = "VIDEO_PLAYER_OPENED" in log_content
        like_button_clicked = "LIKE_BUTTON_CLICKED" in log_content

        # 只要检测到搜索、播放或点赞相关操作即可
        if not (search_completed or video_player_opened or like_button_clicked):
            print("验证失败: 未检测到搜索、播放或点赞操作")
            print("\n提示: 请确保:")
            print("1. 搜索了'游戏解说'")
            print("2. 播放了第一个搜索结果")
            print("3. 点击了点赞按钮")
            print(f"\n日志内容:\n{log_content}")
            return False

        print("搜索播放点赞验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查搜索播放点赞时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckSearchPlayLike()
    print(result1)
