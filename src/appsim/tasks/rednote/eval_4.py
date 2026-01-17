# eval_4.py
import json
import os
import subprocess
from io import StringIO


def like_collect_comment_check(result=None, device_id=None, backup_dir=None):
    output_buffer = StringIO()

    _USER_ID = "user_current"
    _NOTE_KEYWORD = "穿搭"

    try:
        # 从设备获取点赞记录
        likes_file_path = os.path.join(backup_dir, "likes.json") if backup_dir is not None else "likes.json"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/likes.json"])
        with open(likes_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        # 从设备获取收藏记录
        collections_file_path = os.path.join(backup_dir,
                                             "collections.json") if backup_dir is not None else "collections.json"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/collections.json"])
        with open(collections_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        # 从设备获取评论记录
        comments_file_path = os.path.join(backup_dir, "comments.json") if backup_dir is not None else "comments.json"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/comments.json"])
        with open(comments_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        # 从设备获取浏览历史（用于获取笔记信息）
        browsing_file_path = os.path.join(backup_dir,
                                          "browsing_history.json") if backup_dir is not None else "browsing_history.json"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/browsing_history.json"])
        with open(browsing_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        # 读取并解析数据
        try:
            with open(likes_file_path, "r", encoding="utf-8") as f:
                likes_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        try:
            with open(collections_file_path, "r", encoding="utf-8") as f:
                collections_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        # comments.json 可能不存在，如果不存在则为空列表
        try:
            with open(comments_file_path, "r", encoding="utf-8") as f:
                comments_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            comments_data = []

        # 从浏览历史中提取笔记信息
        try:
            with open(browsing_file_path, "r", encoding="utf-8") as f:
                browsing_data = json.load(f)
            # 从浏览历史中构建笔记列表
            notes_data = []
            seen_note_ids = set()
            for item in browsing_data:
                note_id = item.get("noteId")
                if note_id and note_id not in seen_note_ids:
                    notes_data.append({"id": note_id, "title": item.get("noteTitle", "")})
                    seen_note_ids.add(note_id)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        # 查找标题包含关键词的笔记
        target_notes = [note for note in notes_data if _NOTE_KEYWORD in note.get("title", "")]

        if not target_notes:
            return False

        # 检查这些笔记是否被点赞、收藏和评论
        for note in target_notes:
            note_id = note.get("id")

            has_liked = any(
                like.get("userId") == _USER_ID and like.get("targetId") == note_id for like in likes_data
            )

            # 检查收藏
            has_collected = any(
                col.get("userId") == _USER_ID and col.get("noteId") == note_id for col in collections_data
            )

            # 检查评论（内容为"很有用！"）
            has_commented = any(
                comment.get("author", {}).get("id") == _USER_ID
                and comment.get("noteId") == note_id
                and comment.get("content") == "很有用！"
                for comment in comments_data
            )

            # 如果找到一个笔记同时满足三个条件，返回 True
            if has_liked and has_collected and has_commented:
                return True

        return False

    finally:
        output_buffer.close()


if __name__ == "__main__":
    print(like_collect_comment_check())