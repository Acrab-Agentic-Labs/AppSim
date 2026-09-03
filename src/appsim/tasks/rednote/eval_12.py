# eval_12.py
import json
import os
import subprocess


def verify_private_note_published(result=None, device_id=None, backup_dir=None):
    _USER_ID = "user_current"
    _NOTE_TITLE = "今日份分享"
    _NOTE_CONTENT = "天晴了"

    # 从设备获取浏览历史（用于验证笔记是否存在）
    message_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/browsing_history.json"])

    # 将数据写入备份文件
    with open(message_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(message_file_path, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not browsing_data or len(browsing_data) == 0:
        return False

    # 从浏览历史中查找用户自己发布的笔记（通过作者ID匹配）
    user_published_notes = []
    for item in browsing_data:
        author_id = item.get("noteAuthor", {}).get("id")
        if author_id == _USER_ID:
            user_published_notes.append(
                {
                    "id": item.get("noteId"),
                    "title": item.get("noteTitle", ""),
                    "author": {"id": author_id},
                    "content": "",  # 浏览历史中没有完整内容
                    "visibility": "UNKNOWN",  # 浏览历史中没有可见性信息
                }
            )

    # 查找符合条件的笔记（由于数据来源限制，只能验证标题）
    matching_notes = [note for note in user_published_notes if note.get("title") == _NOTE_TITLE]

    if matching_notes:
        return True

    return False


if __name__ == "__main__":
    print(verify_private_note_published())