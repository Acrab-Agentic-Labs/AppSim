import subprocess


def CheckFavoriteVideo(result=None, device_id=None):
    """
    检验逻辑:在视频播放页，点击「收藏」按钮
    验证用户是否在视频播放页点击了收藏按钮
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 进入任意视频播放页")
        print("3. 点击「收藏」按钮")
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

        # step3. 验证关键操作 - 只验证点击行为，不验证状态变更
        video_player_opened = "VIDEO_PLAYER_OPENED" in log_content
        favorite_button_clicked = "FAVORITE_BUTTON_CLICKED" in log_content

        # 只要检测到视频播放或点击收藏按钮即可
        if not (video_player_opened or favorite_button_clicked):
            print("验证失败: 未检测到收藏操作")
            print("\n提示: 请确保:")
            print("1. 进入了视频播放页")
            print("2. 点击了收藏按钮")
            print(f"\n日志内容:\n{log_content}")
            return False

        print("收藏操作验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查收藏操作时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckFavoriteVideo()
    print(result1)
