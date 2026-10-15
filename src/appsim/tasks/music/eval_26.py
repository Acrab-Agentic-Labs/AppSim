"""
任务26：使用听歌识曲功能识别一首歌曲
难度：高
验证：识曲完成后 App 会写入 shared_prefs/recognition_history.xml（清除数据后不存在）
"""

import json
import logging
import subprocess
import xml.etree.ElementTree as ET

from .verification_functions import APP_PACKAGE

RECOGNITION_PREFS = "shared_prefs/recognition_history.xml"


def read_recognition_records(device_id=None):
    """Return recognition records from the app's SharedPreferences, or [] if none exist."""
    cmd = ["adb"] + (["-s", device_id] if device_id else [])
    cmd += ["exec-out", "run-as", APP_PACKAGE, "cat", RECOGNITION_PREFS]
    completed = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if completed.returncode != 0 or not completed.stdout.lstrip().startswith("<?xml"):
        return []
    records = ET.fromstring(completed.stdout).find("string[@name='records']")
    return json.loads(records.text) if records is not None and records.text else []


def verify_song_recognition_attempted(result=None, device_id=None, backup_dir=None):
    records = read_recognition_records(device_id)
    if records:
        logging.info(f"✓ 任务26通过：识曲记录 {len(records)} 条，最新: {records[-1].get('songName')}")
        return True
    logging.warning("✗ 任务26失败：未找到识曲记录")
    return False


if __name__ == "__main__":
    print(verify_song_recognition_attempted())
