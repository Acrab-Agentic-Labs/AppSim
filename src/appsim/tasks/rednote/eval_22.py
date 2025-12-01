# eval_22.py
import json
import os
import subprocess


def count_author_notes_check(result=None, device_id=None, backup_dir=None):
    _AUTHOR_USERNAME = "旅行日记"
    _MIN_COUNT = 0

    # 从设备获取浏览历史（用于获取笔记信息）
    browsing_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    with open(browsing_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    # 从设备获取用户列表
    users_file_path = os.path.join(backup_dir, "users.json") if backup_dir is not None else "users.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/users.json"])
    with open(users_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(browsing_file_path, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)
        with open(users_file_path, "r", encoding="utf-8") as f:
            users_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    # 查找指定昵称的博主
    target_author = None
    for user in users_data:
        if user.get("nickname") == _AUTHOR_USERNAME:
            target_author = user
            break

    if not target_author:
        return False

    author_id = target_author.get("id")

    # 统计该博主的笔记数量
    author_notes = [note for note in browsing_data if note.get("noteAuthor", {}).get("id") == author_id]
    note_count = len(author_notes)

    if note_count >= _MIN_COUNT:
        return True
    else:
        return False


if __name__ == "__main__":
    print(count_author_notes_check())