import subprocess


def CheckFullscreen(result=None, device_id=None):
    """
    检验逻辑:在视频播放页面，点击全屏按钮，进入全屏模式观看
    验证用户是否进入全屏模式
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
        print("3. 点击全屏按钮")
        print("4. 进入全屏模式观看")
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

        # step3. 验证关键操作 - 只需要检测到进入全屏模式即可
        fullscreen_entered = "FULLSCREEN_MODE_ENTERED" in log_content
        fullscreen_clicked = "FULLSCREEN_BUTTON_CLICKED" in log_content

        if not (fullscreen_entered or fullscreen_clicked):
            print("验证失败: 未检测到进入全屏模式")
            print("\n提示: 请确保:")
            print("1. 在视频播放页点击了全屏按钮")
            print("2. 已进入全屏模式")
            return False

        print("全屏模式验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查全屏模式时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckFullscreen()
    print(result1)
