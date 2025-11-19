import json
import subprocess
from io import StringIO


def ReplyCommentCheck(userId="user_current", replyContent="谢谢喜欢～", result=None, device_id=None):
    # 使用StringIO捕获输出，避免修改全局stdout
    output_buffer = StringIO()
    """
    检查用户是否回复了最新收到的评论
    任务6: 查看"消息"->"评论和@"页面，回复最新收到的一条评论，内容为"谢谢喜欢～"
    """
    # 从设备获取评论列表
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["adb", "exec-out", "run-as", "com.example.test05", "cat", "files/comments.json"],
    )
    result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    # comments.json 可能不存在，需要容错处理
    if result1.returncode != 0 or not result1.stdout or not result1.stdout.strip():
        print(" Failed to read comments file")
        print("   Reason: Comments file does not exist or is empty")
        print("   Note: Please add a comment first to create the file")
        if result1.stderr:
            print(f"   Error: {result1.stderr}")
        return False

    # 解析 JSON
    try:
        data = json.loads(result1.stdout.strip())
    except:
        print(" Failed to parse comments data")
        print("   Reason: Invalid JSON format")
        return False

    # 检查评论回复
    try:
        if not data or len(data) == 0:
            print(" Comments list is empty")
            print("   Reason: No comments found")
            return False

        # 查找回复类型的评论（parentCommentId不为空表示是回复）
        replies = [
            comment
            for comment in data
            if comment.get("author", {}).get("id") == userId
            and comment.get("parentCommentId") is not None
            and comment.get("content") == replyContent
        ]

        # 如果找到符合条件的回复，返回 True
        if replies:
            latest_reply = sorted(replies, key=lambda x: x.get("createdAt", ""), reverse=True)[0]
            if latest_reply.get("content") == replyContent:
                print(f"✓ Successfully replied with '{replyContent}'")
                return True

        print(" Reply comment not found")
        print(f"   Reason: No reply with content '{replyContent}' from user '{userId}'")
        # Show recent replies
        user_replies = [
            c.get("content", "UNKNOWN")
            for c in data
            if c.get("author", {}).get("id") == userId and c.get("parentCommentId") is not None
        ][:3]
        if user_replies:
            print(f"   Recent replies: {user_replies}")
        return False

    except:
        print(" Error while checking reply comments")
        return False
    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(ReplyCommentCheck(userId="user_current", replyContent="谢谢喜欢～"))
