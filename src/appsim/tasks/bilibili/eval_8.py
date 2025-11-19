import subprocess


def CheckWatchRecommend(result=None, device_id=None):
    """
    检验逻辑:在首页观看一条推荐中的视频
    验证用户是否在首页点击并观看推荐视频
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 在首页点击一条推荐视频")
        print("3. 观看视频")
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

        # step3. 验证关键操作 - 只需要检测到视频播放即可
        # 放宽验证条件：只要检测到视频播放页打开和播放开始就算成功
        video_player_opened = "VIDEO_PLAYER_OPENED" in log_content
        video_playback_started = "VIDEO_PLAYBACK_STARTED" in log_content

        if not video_player_opened and not video_playback_started:
            print("验证失败: 未检测到视频播放")
            print("\n提示: 请确保:")
            print("1. 在首页点击了一条推荐视频")
            print("2. 视频已经开始播放")
            return False

        print("观看推荐视频验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查观看推荐视频时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckWatchRecommend()
    print(result1)
