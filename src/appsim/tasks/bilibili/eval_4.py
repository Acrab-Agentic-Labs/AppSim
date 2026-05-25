import subprocess


TASK4_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取追番列表中第一个动漫的名称。",
    "properties": {
        "anime_name": {
            "type": "string",
            "description": "追番列表中第一个动漫的完整名称。",
        }
    },
    "required": ["anime_name"],
    "additionalProperties": False,
}


def CheckProfilePage(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    anime_name = str(extracted_answer.get("anime_name") or "")
    if "凡人修仙传" not in anime_name:
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

        if 'PROFILE_DATA_LOADED' not in log_content:
            return False

        return True

    except Exception:
        return False
