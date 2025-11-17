import subprocess


def CheckLikeVideo(result=None, device_id=None):
    """
    检验逻辑:在视频播放页，点击「点赞」按钮
    验证用户是否在视频播放页点击了点赞按钮
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
        print("3. 点击「点赞」按钮")
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

        # step3. 验证是否进入视频播放页
        if "VIDEO_PLAYER_OPENED" not in log_content:
            print("验证失败: 未检测到进入视频播放页")
            print(f"日志内容:\n{log_content}")
            return False

        # step4. 验证是否点击了点赞按钮
        if "LIKE_BUTTON_CLICKED" not in log_content:
            print("验证失败: 未检测到点击点赞按钮")
            print(f"日志内容:\n{log_content}")
            return False

        # step5. 验证点赞状态是否更新
        if "LIKE_STATUS_CHANGED" not in log_content or "liked" not in log_content:
            print("验证失败: 点赞状态未更新")
            print(f"日志内容:\n{log_content}")
            return False

        print("点赞操作验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查点赞操作时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckLikeVideo()
    print(result1)
