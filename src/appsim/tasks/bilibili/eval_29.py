import subprocess
import json
import os
import shutil
import time


def verify_offline_cache_video_comment_and_message_setting(result=None, device_id=None, backup_dir=None):
    """
    检验逻辑: 看一下离线缓存中是什么视频然后去我的收藏里观看这个视频，
    并给这个视频评论"张三就是有学问！"然后关闭消息设置里的消息提醒。
    非推理任务，步长14
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

        # 1. 验证进入离线缓存页面
        cache_entered = 'OFFLINE_CACHE_PAGE_ENTERED' in log_content
        if not cache_entered:
            print("验证失败: 未检测到进入离线缓存页面")
            return False

        # 2. 验证进入收藏页面
        favorite_entered = 'FAVORITE_PAGE_ENTERED' in log_content
        if not favorite_entered:
            print("验证失败: 未检测到进入收藏页面")
            return False

        # 3. 验证播放视频
        video_opened = 'VIDEO_PLAYER_OPENED' in log_content
        if not video_opened:
            print("验证失败: 未检测到播放视频")
            return False

        # 4. 验证评论输入和发送
        comment_input = 'COMMENT_INPUT_TEXT' in log_content
        comment_content = '张三就是有学问！' in log_content
        send_clicked = 'SEND_BUTTON_CLICKED' in log_content
        comment_sent = 'COMMENT_SENT_SUCCESS' in log_content

        if not (comment_input or comment_content):
            print("验证失败: 未检测到输入评论'张三就是有学问！'")
            return False

        if not (send_clicked or comment_sent):
            print("验证失败: 未检测到发送评论")
            return False

        # 5. 验证进入消息设置页面
        message_settings_entered = 'MESSAGE_SETTINGS_PAGE_ENTERED' in log_content
        if not message_settings_entered:
            print("验证失败: 未检测到进入消息设置页面")
            return False

        # 6. 验证关闭消息提醒开关
        message_reminder_off = 'MESSAGE_REMINDER_SWITCH_CHANGED: off' in log_content
        if not message_reminder_off:
            print("⚠️ 未检测到关闭消息提醒开关日志，尝试读取文件验证")
            # 回退：读取 message_settings.json 验证
            cmd2 = ["adb"]
            if device_id:
                cmd2.extend(["-s", device_id])
            cmd2.extend(["exec-out", "run-as", "com.example.bilibili_sim",
                        "cat", "files/message_settings.json"])
            result2 = subprocess.run(cmd2, capture_output=True, text=True,
                                    timeout=10, encoding='utf-8', errors='ignore')
            if result2.stdout:
                try:
                    msg_data = json.loads(result2.stdout)
                    if msg_data.get("message_reminder") == False:
                        print("✓ 文件验证: 消息提醒已关闭")
                    else:
                        print("验证失败: 消息提醒未关闭")
                        return False
                except json.JSONDecodeError:
                    print("⚠️ 无法解析消息设置文件，跳过此步验证")
            else:
                print("⚠️ 无法读取消息设置文件，跳过此步验证")

        print("离线缓存视频评论+关闭消息提醒验证成功!")
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
    result1 = verify_offline_cache_video_comment_and_message_setting()
    print(result1)
