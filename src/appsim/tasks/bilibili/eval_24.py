import subprocess


TASK24_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取用户的UID。",
    "properties": {
        "uid": {
            "type": "string",
            "description": "用户的UID数字字符串。",
        }
    },
    "required": ["uid"],
    "additionalProperties": False,
}


def verify_uid_and_chat_push_closed(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    uid = str(extracted_answer.get("uid") or "")
    if "649734343" not in uid:
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

        if 'CHAT_MESSAGE_SWITCH_CHANGED: off' not in log_content:
            return False

        return True

    except Exception:
        return False
