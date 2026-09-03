# eval_6.py
import json
import os
import subprocess
from io import StringIO


def verify_latest_comment_replied(result=None, device_id=None, backup_dir=None):
    output_buffer = StringIO()

    _USER_ID = "user_current"
    _REPLY_CONTENT = "谢谢喜欢～"

    try:
        # 从设备获取评论列表
        message_file_path = os.path.join(backup_dir, "comments.json") if backup_dir is not None else "comments.json"

        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/comments.json"])

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

        # 查找回复类型的评论（parentCommentId不为空表示是回复）
        replies = [
            comment
            for comment in data
            if comment.get("author", {}).get("id") == _USER_ID
               and comment.get("parentCommentId") is not None
               and comment.get("content") == _REPLY_CONTENT
        ]

        # 如果找到符合条件的回复，返回 True
        if replies:
            latest_reply = sorted(replies, key=lambda x: x.get("createdAt", ""), reverse=True)[0]
            if latest_reply.get("content") == _REPLY_CONTENT:
                return True

        return False

    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(verify_latest_comment_replied())