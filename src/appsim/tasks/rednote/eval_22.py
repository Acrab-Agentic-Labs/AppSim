# eval_22.py
import json
import os
import subprocess

TASK22_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取博主'旅行日记'发布的笔记数量。",
    "properties": {
        "note_count": {
            "type": "integer",
            "description": "该博主发布的笔记数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["note_count"],
    "additionalProperties": False,
}


def count_author_notes_check(result=None, device_id=None, backup_dir=None):
    _AUTHOR_USERNAME = "旅行日记"

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    note_count_answer = extracted_answer.get("note_count")
    if note_count_answer is None:
        return False

    notes_file_path = os.path.join(backup_dir, "notes.json") if backup_dir is not None else "notes.json"
    users_file_path = os.path.join(backup_dir, "users.json") if backup_dir is not None else "users.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/notes.json"])
        with open(notes_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/users.json"])
        with open(users_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(notes_file_path, "r", encoding="utf-8") as f:
            notes_data = json.load(f)
        with open(users_file_path, "r", encoding="utf-8") as f:
            users_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    target_author = None
    for user in users_data:
        if user.get("nickname") == _AUTHOR_USERNAME:
            target_author = user
            break

    if not target_author:
        return False

    author_id = target_author.get("id")
    expected = sum(1 for note in notes_data if note.get("authorId") == author_id)

    return note_count_answer == expected


if __name__ == "__main__":
    print(count_author_notes_check())