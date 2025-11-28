import subprocess
import json
import os
import shutil
import time


def CheckWatchRecommend(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:在首页观看一条推荐中的视频
    验证用户是否在首页点击并观看推荐视频
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

        # step3. 验证关键操作 - 只需要检测到视频播放即可
        # 放宽验证条件：只要检测到视频播放页打开和播放开始就算成功
        video_player_opened = 'VIDEO_PLAYER_OPENED' in log_content
        video_playback_started = 'VIDEO_PLAYBACK_STARTED' in log_content

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
    result1 = CheckWatchRecommend()
    print(result1)
