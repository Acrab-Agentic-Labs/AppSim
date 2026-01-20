# eval_7.py
import json
import os
import subprocess


def browsing_history_check(result=None, device_id=None, backup_dir=None):
    message_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/browsing_history.json"])

    # 从设备获取文件并写入备份
    with open(message_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    # 获取最后一条数据
    last_item = data[-1]

    # 检查 noteAuthor.id 和 noteTitle
    if (
            last_item.get("noteAuthor", {}).get("id") == "user_002"
            and last_item.get("noteTitle") == "穿搭灵感 | 秋冬穿搭必备单品清单，照着买不出错！"
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    print(browsing_history_check())