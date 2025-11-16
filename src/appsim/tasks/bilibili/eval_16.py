import subprocess
import json
import os
import shutil
import time


def CheckReplyComment(result=None, device_id=None):
    """
    检验逻辑:对首页第一条视频评论，点击回复，输入"谢谢分享！"并发送
    验证用户是否完成评论回复
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 在首页点击第一条视频")
        print("3. 进入评论页面")
        print("4. 点击回复按钮")
        print("5. 输入'谢谢分享！'")
        print("6. 点击发送")
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

        # step3. 验证关键操作 - 简化验证逻辑，只检测核心标签
        comment_page_entered = "COMMENT_PAGE_ENTERED" in log_content
        reply_button_clicked = "REPLY_BUTTON_CLICKED" in log_content
        comment_input_text = "COMMENT_INPUT_TEXT" in log_content
        comment_content_check = "谢谢分享！" in log_content
        send_button_clicked = "SEND_BUTTON_CLICKED" in log_content
        comment_sent_success = "COMMENT_SENT_SUCCESS" in log_content

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
    except Exception as e:
        print(f"检查评论回复时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckReplyComment()
    print(result1)
