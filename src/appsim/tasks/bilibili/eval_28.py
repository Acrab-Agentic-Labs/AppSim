import subprocess
import os


def validate_task_28(result=None, device_id=None, backup_dir=None):
    """
    任务28: 算一下我的关注列表里的前五个关注一共发了多少条视频，然后去导航栏的关注动态页面，在列表页面给逍遥散人的第一条动态点赞！
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 推理部分：检查 final_message 中是否包含视频总数 378
    if '378' not in final_message:
        return False

    # 操作部分：检查日志中是否给逍遥散人的动态点赞
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

        follow_page = 'FOLLOW_PAGE_ENTERED' in log_content
        xiaoyao_liked = 'DYNAMIC_LIKE_CLICKED: up_xiaoyao' in log_content

        if not (follow_page and xiaoyao_liked):
            return False

        return True

    except Exception:
        return False


if __name__ == '__main__':
    result = validate_task_28()
    print(result)
