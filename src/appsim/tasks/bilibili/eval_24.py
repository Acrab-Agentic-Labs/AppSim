import subprocess
import os


def CheckUidAndCloseChatPush(result=None, device_id=None, backup_dir=None):
    """
    任务24: 查看我的Uid并关闭推送设置中的聊天消息
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 推理部分：检查 final_message 中是否包含 UID
    if '649734343' not in final_message:
        return False

    # 操作部分：检查日志中是否关闭了聊天消息
    try:
        cmd_logcat = ['adb']
        if device_id:
            cmd_logcat.extend(['-s', device_id])
        cmd_logcat.extend(['logcat', '-d', '-s', 'BilibiliAutoTest:D'])

        log_result = subprocess.run(
            cmd_logcat,
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='ignore'
        )
        log_content = log_result.stdout

        if 'CHAT_MESSAGE_SWITCH_CHANGED: off' not in log_content:
            return False

        return True

    except Exception:
        return False


if __name__ == '__main__':
    result = CheckUidAndCloseChatPush()
    print(result)
