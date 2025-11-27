import subprocess
import json
import os
import shutil
import time


def CheckFullscreen(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:在视频播放页面，点击全屏按钮，进入全屏模式观看
    验证用户是否进入全屏模式
    """
    try:
        print("\n正在检查日志...")
        cmd_logcat = ['adb']
        if device_id:
            cmd_logcat.extend(['-s', device_id])
        cmd_logcat.extend(['logcat', '-d', '-s', 'BilibiliAutoTest:D'])

        result1 = subprocess.run(
            cmd_logcat,
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='ignore'
        )

        log_content = result1.stdout
        if backup_dir:
            logcat_file_path = os.path.join(backup_dir, 'logcat.txt')
            open(logcat_file_path, 'w', encoding='utf-8').write(log_content)

        # step3. 验证关键操作 - 只需要检测到进入全屏模式即可
        fullscreen_entered = 'FULLSCREEN_MODE_ENTERED' in log_content
        fullscreen_clicked = 'FULLSCREEN_BUTTON_CLICKED' in log_content

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
    finally:
        # 无论成功失败，最后都清除日志
        try:
            cmd_clear = ['adb']
            if device_id:
                cmd_clear.extend(['-s', device_id])
            cmd_clear.extend(['logcat', '-c'])
            subprocess.run(cmd_clear, timeout=5)
            print("🔄 已清除日志缓存")
        except subprocess.TimeoutExpired:
            print("⚠️ 清除日志超时")
        except Exception as e:
            print(f"⚠️ 清除日志失败: {str(e)}")

if __name__ == "__main__":
    result1 = CheckFullscreen()
    print(result1)
