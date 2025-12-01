# eval_15.py
import json
import os
import subprocess


def like_comment_check(result=None, device_id=None, backup_dir=None):
    _USER_ID = "user_current"

    # 从设备获取点赞记录
    message_file_path = os.path.join(backup_dir, "likes.json") if backup_dir is not None else "likes.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/likes.json"])

    # 将数据写入备份文件
    with open(message_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not data or len(data) == 0:
        return False

    # 查找用户对评论的点赞记录
    comment_likes = [
        like for like in data if like.get("userId") == _USER_ID and like.get("targetType") == "COMMENT"
    ]

    # 如果有最新的评论点赞记录，返回 True
    if comment_likes:
        return True

    return False


if __name__ == "__main__":
    print(like_comment_check())