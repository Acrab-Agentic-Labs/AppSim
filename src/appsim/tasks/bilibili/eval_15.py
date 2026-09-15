import subprocess
import os


TASK15_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取删除历史记录后剩余的视频数量。",
    "properties": {
        "remaining_count": {
            "type": "integer",
            "description": "删除后剩余的视频数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["remaining_count"],
    "additionalProperties": False,
}


def verify_history_item_deleted(result=None, device_id=None, backup_dir=None):
    try:
        cmd_logcat = ['adb']
        if device_id:
            cmd_logcat.extend(['-s', device_id])
        cmd_logcat.extend(['logcat', '-d', '-s', 'BilibiliAutoTest:D'])

        result1 = subprocess.run(
            cmd_logcat,
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='ignore'
        )

        log_content = result1.stdout
        if backup_dir:
            logcat_file_path = os.path.join(backup_dir, 'logcat.txt')
            open(logcat_file_path, 'w', encoding='utf-8').write(log_content)

        history_item_long_pressed = 'HISTORY_ITEM_LONG_PRESSED' in log_content
        delete_button_clicked = 'DELETE_BUTTON_CLICKED' in log_content
        history_item_deleted = 'HISTORY_ITEM_DELETED' in log_content

        if not (history_item_long_pressed or delete_button_clicked or history_item_deleted):
            return False

        if not isinstance(result, dict):
            return False
        extracted_answer = result.get("extracted_answer")
        if not isinstance(extracted_answer, dict):
            return False
        remaining_count = extracted_answer.get("remaining_count")
        return remaining_count == 8

    except subprocess.TimeoutExpired:
        return False
