import subprocess
import os


def CheckSearchCountAndRelated(result=None, device_id=None, backup_dir=None):
    """
    检验逻辑:搜索"游戏解说"，播放第一个视频查看相关视频有几个，告诉我答案即可
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 推理部分：检查 final_message 中是否包含 "4"
    if '4' not in final_message:
        return False

    # 操作部分：检查日志中是否搜索并播放了视频
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

        if 'SEARCH_INPUT' not in log_content or '游戏解说' not in log_content:
            return False

        if 'VIDEO_PLAYER_OPENED' not in log_content:
            return False

        return True

    except Exception:
        return False


if __name__ == "__main__":
    result = CheckSearchCountAndRelated()
    print(result)
