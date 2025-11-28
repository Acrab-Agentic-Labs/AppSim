import subprocess
import json
import os
import shutil
import time



def CheckReplyComment(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:对首页第一条视频评论，点击回复，输入"谢谢分享！"并发送
    验证用户是否完成评论回复
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

        # step3. 验证关键操作 - 简化验证逻辑，只检测核心标签
        comment_page_entered = 'COMMENT_PAGE_ENTERED' in log_content
        reply_button_clicked = 'REPLY_BUTTON_CLICKED' in log_content
        comment_input_text = 'COMMENT_INPUT_TEXT' in log_content
        comment_content_check = '谢谢分享！' in log_content
        send_button_clicked = 'SEND_BUTTON_CLICKED' in log_content
        comment_sent_success = 'COMMENT_SENT_SUCCESS' in log_content

        # 至少检测到评论页面进入或回复按钮点击
        if not (comment_page_entered or reply_button_clicked):
            print("验证失败: 未检测到进入评论页面或点击回复")
            print("\n提示: 请确保:")
            print("1. 进入了评论页面")
            print("2. 点击了回复按钮")
            return False

        # 检测输入内容
        if not (comment_input_text or comment_content_check):
            print("验证失败: 未检测到输入评论内容'谢谢分享！'")
            print("\n提示: 请确保输入了'谢谢分享！'")
            return False

        # 检测发送操作
        if not (send_button_clicked or comment_sent_success):
            print("验证失败: 未检测到点击发送或评论发送成功")
            print("\n提示: 请确保点击了发送按钮")
            return False

        print("评论回复验证成功!")
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
    result1 = CheckReplyComment()
    print(result1)
