# eval_17.py
import json
import os
import subprocess


def search_result_count_check(result=None, device_id=None, backup_dir=None):
    _USER_ID = "user_current"
    _SEARCH_QUERY = "美妆"
    _MIN_COUNT = 1

    # 从设备获取搜索历史
    search_file_path = os.path.join(backup_dir, "search_history.json") if backup_dir is not None else "search_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/search_history.json"])
    with open(search_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    # 从设备获取浏览历史（用于获取笔记信息）
    browsing_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    with open(browsing_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(search_file_path, "r", encoding="utf-8") as f:
            search_data = json.load(f)
        with open(browsing_file_path, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    # 检查是否有搜索记录
    if not search_data or len(search_data) == 0:
        return False

    # 查找用户的搜索记录
    user_searches = [
        item for item in search_data if item.get("userId") == _USER_ID and item.get("query") == _SEARCH_QUERY
    ]

    if not user_searches:
        return False

    # 统计包含搜索关键词的笔记数量（仅通过标题匹配）
    matching_notes = [note for note in browsing_data if _SEARCH_QUERY in note.get("noteTitle", "")]
    note_count = len(matching_notes)

    if note_count >= _MIN_COUNT:
        return True
    else:
        return False


if __name__ == "__main__":
    print(search_result_count_check())