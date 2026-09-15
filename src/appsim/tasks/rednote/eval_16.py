# eval_16.py
import json
import os
import subprocess


def verify_homepage_notes_interacted_with(result=None, device_id=None, backup_dir=None):
    _USER_ID = "user_current"
    _VIEW_COUNT = 2
    _COMMENT_CONTENT = "很精彩"

    # 从设备获取浏览历史
    browsing_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/browsing_history.json"])
    with open(browsing_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    # 从设备获取点赞记录
    likes_file_path = os.path.join(backup_dir, "likes.json") if backup_dir is not None else "likes.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/likes.json"])
    with open(likes_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    # 从设备获取收藏记录
    collections_file_path = os.path.join(backup_dir, "collections.json") if backup_dir is not None else "collections.json"
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

    try:
        with open(browsing_file_path, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)
        with open(likes_file_path, "r", encoding="utf-8") as f:
            likes_data = json.load(f)
        with open(collections_file_path, "r", encoding="utf-8") as f:
            collections_data = json.load(f)
        with open(comments_file_path, "r", encoding="utf-8") as f:
            comments_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    # 获取用户从首页浏览的笔记
    home_browsing = [
        item for item in browsing_data if item.get("userId") == _USER_ID and item.get("sourceType") == "HOME_FEED"
    ]

    if len(home_browsing) < _VIEW_COUNT:
        return False

    # 获取最近浏览的N篇笔记
    recent_browsing = sorted(home_browsing, key=lambda x: x.get("browsedAt", ""), reverse=True)[:_VIEW_COUNT]
    note_ids = [item.get("noteId") for item in recent_browsing]

    # 检查这些笔记是否都被点赞、收藏和评论
    success_count = 0
    for note_id in note_ids:
        has_liked = any(
            like.get("userId") == _USER_ID
            and like.get("targetId") == note_id
            and like.get("targetType") == "NOTE"
            for like in likes_data
        )

        has_collected = any(
            col.get("userId") == _USER_ID and col.get("noteId") == note_id for col in collections_data
        )

        has_commented = any(
            comment.get("author", {}).get("id") == _USER_ID
            and comment.get("noteId") == note_id
            and comment.get("content") == _COMMENT_CONTENT
            for comment in comments_data
        )

        if has_liked and has_collected and has_commented:
            success_count += 1

    if success_count >= _VIEW_COUNT:
        return True
    else:
        return False


if __name__ == "__main__":
    print(verify_homepage_notes_interacted_with())