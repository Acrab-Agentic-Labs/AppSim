import subprocess
import json
import os
import shutil
import time


def CheckVideoLikeFavoriteFullscreen(result=None, device_id=None, backup_dir=None):
    """
    检验逻辑:看主页第一个视频，点赞，取消收藏，进入全屏模式观看
    验证用户是否完成点赞、收藏、全屏三个操作
    合并自: eval_5(点赞) + eval_7(收藏) + eval_10(全屏)
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

        # 验证是否进入视频播放页
        video_player_opened = 'VIDEO_PLAYER_OPENED' in log_content
        if not video_player_opened:
            print("验证失败: 未检测到进入视频播放页")
            print(f"日志内容:\n{log_content}")
            return False

        # 验证是否点击了点赞按钮
        like_button_clicked = 'LIKE_BUTTON_CLICKED' in log_content
        if not like_button_clicked:
            print("验证失败: 未检测到点击点赞按钮")
            return False

        # 验证是否点击了收藏按钮
        favorite_button_clicked = 'FAVORITE_BUTTON_CLICKED' in log_content
        if not favorite_button_clicked:
            print("验证失败: 未检测到点击收藏按钮")
            return False

        # 验证是否进入全屏模式
        fullscreen_entered = 'FULLSCREEN_MODE_ENTERED' in log_content
        fullscreen_clicked = 'FULLSCREEN_BUTTON_CLICKED' in log_content
        if not (fullscreen_entered or fullscreen_clicked):
            print("验证失败: 未检测到进入全屏模式")
            return False

        print("点赞+收藏+全屏验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    finally:
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
    result1 = CheckVideoLikeFavoriteFullscreen()
    print(result1)
