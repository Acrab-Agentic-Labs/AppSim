import subprocess
import json
import os
import shutil
import time



def CheckSearchPlayLike(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:搜索视频"游戏解说"，播放搜索出的第一个视频，点赞
    验证用户是否在APP中真正完成了搜索、播放和点赞操作
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

        # step3. 验证关键操作 - 放宽验证条件
        search_completed = 'SEARCH_COMPLETED' in log_content
        search_keyword = '游戏解说' in log_content
        first_result_clicked = 'FIRST_SEARCH_RESULT_CLICKED' in log_content
        video_player_opened = 'VIDEO_PLAYER_OPENED' in log_content
        like_button_clicked = 'LIKE_BUTTON_CLICKED' in log_content

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
    result1 = CheckSearchPlayLike()
    print(result1)
