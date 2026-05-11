import subprocess
import os


def CheckProfilePage(result=None, device_id=None, backup_dir=None):
    """
    任务4: 进入我的个人资料页查看我追的第一个动漫叫什么
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 推理部分：检查 final_message 中是否包含 "凡人修仙传"
    if '凡人修仙传' not in final_message:
        return False

    # 操作部分：检查日志中是否进入了个人资料页
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

        if 'PROFILE_DATA_LOADED' not in log_content:
            return False

        return True

    except Exception:
        return False


if __name__ == '__main__':
    result = CheckProfilePage()
    print(result)
