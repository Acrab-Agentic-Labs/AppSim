import json
import os
import subprocess
from io import StringIO


def reply_comment_check(result=None, device_id=None, backup_dir=None):
    # 使用StringIO捕获输出，避免修改全局stdout
    output_buffer = StringIO()

    _USER_ID = "user_current"
    _REPLY_CONTENT = "谢谢喜欢～"
    """
    检查用户是否回复了最新收到的评论
    任务6: 查看"消息"->"评论和@"页面，回复最新收到的一条评论，内容为"谢谢喜欢～"
    """
    # 从设备获取评论列表
    message_file_path = os.path.join(backup_dir, "comments.json") if backup_dir is not None else "comments.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/comments.json"])

    # 将数据写入备份文件
    with open(message_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return False

    # 检查评论回复
    try:
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

    except:
        return False
    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(reply_comment_check())