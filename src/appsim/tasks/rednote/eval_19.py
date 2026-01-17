# eval_19.py
import json
import os
import subprocess


def note_interaction_check(result=None, device_id=None, backup_dir=None):
    # 检查浏览历史
    browsing_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/browsing_history.json"])
    with open(browsing_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(browsing_file_path, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not browsing_data or len(browsing_data) == 0:
        return False

    last_browsing = browsing_data[-1]
    browsing_author_id = last_browsing.get("noteAuthor", {}).get("id", "")
    browsing_title = last_browsing.get("noteTitle", "")

    if not (browsing_author_id == "user_003" and browsing_title == "AI技术在日常生活中的应用，太实用了！"):
        return False

    # 检查点赞记录
    likes_file_path = os.path.join(backup_dir, "likes.json") if backup_dir is not None else "likes.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/likes.json"])
    with open(likes_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(likes_file_path, "r", encoding="utf-8") as f:
            likes_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not likes_data or len(likes_data) == 0:
        return False

    last_like = likes_data[-1]
    like_target_id = last_like.get("targetId", "")

    if like_target_id != "note_002":
        return False

    # 检查评论记录
    comments_file_path = os.path.join(backup_dir, "comments.json") if backup_dir is not None else "comments.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/comments.json"])
    with open(comments_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(comments_file_path, "r", encoding="utf-8") as f:
            comments_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not comments_data or len(comments_data) == 0:
        return False

    last_comment = comments_data[-1]
    comment_content = last_comment.get("content", "")
    comment_note_id = last_comment.get("noteId", "")

    if not (comment_content == "很实用！" and comment_note_id == "note_002"):
        return False

    # 所有检查都通过
    return True


if __name__ == "__main__":
    print(note_interaction_check())