import subprocess


TASK28_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取关注列表前五个关注一共发了多少条视频。",
    "properties": {
        "total_videos": {
            "type": "integer",
            "description": "前五个关注发布的视频总数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total_videos"],
    "additionalProperties": False,
}


def validate_task_28(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    total_videos = extracted_answer.get("total_videos")
    if total_videos != 378:
        return False

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
