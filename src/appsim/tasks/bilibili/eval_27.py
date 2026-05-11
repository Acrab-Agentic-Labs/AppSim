import subprocess
import os


def validate_task_27(result=None, device_id=None, backup_dir=None):
    """
    任务27: 分别打开历史记录里的第二个视频和收藏夹里的第二个视频，查看各自评论区展示的第一条一级评论的点赞数；
    如果两者不同，就对点赞数更高的那个视频发送评论"这赞也太多了吧！"，如果两者相同，就对历史记录里的那个视频发送评论。
    验证: 检查日志中是否进入了历史记录页，并对收藏夹第二个视频(vid002)发送了评论。
    """
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

        if backup_dir:
            logcat_file_path = os.path.join(backup_dir, 'logcat_38.txt')
            with open(logcat_file_path, 'w', encoding='utf-8') as f:
                f.write(log_content)

        # 1. 验证是否进入了历史记录页
        if 'HISTORY_PAGE_ENTERED' not in log_content:
            return False

        # 2. 验证是否对收藏夹第二个视频(vid002)发送了评论"这赞也太多了吧！"
        if not ('COMMENT_SENT:vid002' in log_content or
                ('COMMENT_SENT_SUCCESS' in log_content and 'vid002' in log_content)):
            return False

        if '这赞也太多了吧！' not in log_content:
            return False

        return True

    except Exception:
        return False


if __name__ == '__main__':
    result = validate_task_27()
    print(result)
