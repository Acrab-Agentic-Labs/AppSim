import subprocess


TASK22_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取搜索'游戏解说'后第一个视频的相关视频数量。",
    "properties": {
        "related_count": {
            "type": "integer",
            "description": "相关视频的数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["related_count"],
    "additionalProperties": False,
}


def CheckSearchCountAndRelated(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    related_count = extracted_answer.get("related_count")
    if related_count != 4:
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

        if 'SEARCH_INPUT' not in log_content or '游戏解说' not in log_content:
            return False

        if 'VIDEO_PLAYER_OPENED' not in log_content:
            return False

        return True

    except Exception:
        return False
