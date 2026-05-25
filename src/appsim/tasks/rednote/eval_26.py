# eval_26.py
import json
import os
import subprocess

TASK26_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取'潮流时尚达人'发布的笔记数量。",
    "properties": {
        "note_count": {
            "type": "integer",
            "description": "该博主发布的笔记数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["note_count"],
    "additionalProperties": False,
}


def eval_26(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    message_file_path = os.path.join(backup_dir, "notes.json") if backup_dir is not None else "notes.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/notes.json"])
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    expected = sum(1 for item in data if item.get("authorId") == "user_002")
    return extracted_answer.get("note_count") == expected


if __name__ == "__main__":
    result = eval_26()
    print(result)
