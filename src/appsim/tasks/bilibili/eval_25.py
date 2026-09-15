import subprocess
import json
import os
import shutil
import time


def verify_favorite_video_like_comment(result=None, device_id=None, backup_dir=None):
    """
    检验逻辑:给我的收藏里第二个视频点赞并评论："谢谢up主的分享！"
    验证用户是否进入收藏、点赞、并发送评论
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

        # 1. 验证进入收藏页面
        favorite_page_entered = 'FAVORITE_PAGE_ENTERED' in log_content
        if not favorite_page_entered:
            print("验证失败: 未检测到进入收藏页面")
            print("\n提示: 请确保进入了我的收藏页面")
            return False

        # 2. 验证点赞操作
        like_button_clicked = 'LIKE_BUTTON_CLICKED' in log_content
        if not like_button_clicked:
            print("验证失败: 未检测到点赞操作")
            print("\n提示: 请确保对视频点击了点赞按钮")
            return False

        # 3. 验证进入评论并输入内容
        comment_page_entered = 'COMMENT_PAGE_ENTERED' in log_content
        reply_button_clicked = 'REPLY_BUTTON_CLICKED' in log_content
        if not (comment_page_entered or reply_button_clicked):
            print("验证失败: 未检测到进入评论页面")
            return False

        # 4. 验证输入评论内容
        comment_input_text = 'COMMENT_INPUT_TEXT' in log_content
        comment_content_check = '谢谢up主的分享！' in log_content
        if not (comment_input_text or comment_content_check):
            print("验证失败: 未检测到输入评论内容'谢谢up主的分享！'")
            return False

        # 5. 验证发送评论
        send_button_clicked = 'SEND_BUTTON_CLICKED' in log_content
        comment_sent_success = 'COMMENT_SENT_SUCCESS' in log_content
        if not (send_button_clicked or comment_sent_success):
            print("验证失败: 未检测到点击发送或评论发送成功")
            return False

        print("收藏视频点赞+评论验证成功!")
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
    result1 = verify_favorite_video_like_comment()
    print(result1)
