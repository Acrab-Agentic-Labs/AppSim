import subprocess
import json
import os
import shutil
import time


def CheckSearchPlayLikeReply(result=None, device_id=None, backup_dir=None):
    """
    检验逻辑:搜索视频"游戏解说"，播放搜索出的第一个视频并点赞，然后对该视频评论"谢谢分享！"
    验证用户是否完成搜索、播放、点赞、评论回复全流程
    合并自: eval_22(搜索播放点赞) + eval_16(评论回复)
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

        # 1. 验证搜索操作
        search_completed = 'SEARCH_COMPLETED' in log_content
        search_keyword = '游戏解说' in log_content
        if not (search_completed or search_keyword):
            print("验证失败: 未检测到搜索'游戏解说'")
            print(f"日志内容:\n{log_content}")
            return False

        # 2. 验证播放视频
        video_player_opened = 'VIDEO_PLAYER_OPENED' in log_content
        if not video_player_opened:
            print("验证失败: 未检测到播放视频")
            return False

        # 3. 验证点赞
        like_button_clicked = 'LIKE_BUTTON_CLICKED' in log_content
        if not like_button_clicked:
            print("验证失败: 未检测到点击点赞按钮")
            return False

        # 4. 验证进入评论页面
        comment_page_entered = 'COMMENT_PAGE_ENTERED' in log_content
        reply_button_clicked = 'REPLY_BUTTON_CLICKED' in log_content
        if not (comment_page_entered or reply_button_clicked):
            print("验证失败: 未检测到进入评论页面或点击回复")
            return False

        # 5. 验证输入评论内容
        comment_input_text = 'COMMENT_INPUT_TEXT' in log_content
        comment_content_check = '谢谢分享！' in log_content
        if not (comment_input_text or comment_content_check):
            print("验证失败: 未检测到输入评论内容'谢谢分享！'")
            return False

        # 6. 验证发送评论
        send_button_clicked = 'SEND_BUTTON_CLICKED' in log_content
        comment_sent_success = 'COMMENT_SENT_SUCCESS' in log_content
        if not (send_button_clicked or comment_sent_success):
            print("验证失败: 未检测到点击发送或评论发送成功")
            return False

        print("搜索播放点赞+评论回复全流程验证成功!")
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
    result1 = CheckSearchPlayLikeReply()
    print(result1)
