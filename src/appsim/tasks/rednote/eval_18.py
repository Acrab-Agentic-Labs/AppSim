import json
import os
import subprocess


def publish_and_self_interact_check(result=None, device_id=None, backup_dir=None):
    """
    检查用户是否发布了指定笔记并对其进行点赞和收藏
    任务18: 点击底部栏的"+"号，点击添加图片，并输入文字"今天也要加油呀"，
           进入下一步，添加标题为"今日分享"，笔记设为"公开可见"，最后发布笔记并对这篇笔记进行点赞、收藏
    """
    _USER_ID = "user_current"
    _NOTE_TITLE = "今日分享"

    # 从设备获取浏览历史（用于验证笔记）
    browsing_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    with open(browsing_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    # 从设备获取点赞记录
    likes_file_path = os.path.join(backup_dir, "likes.json") if backup_dir is not None else "likes.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/likes.json"])
    with open(likes_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    # 从设备获取收藏记录
    collections_file_path = os.path.join(backup_dir, "collections.json") if backup_dir is not None else "collections.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/collections.json"])
    with open(collections_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(browsing_file_path, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)
        with open(likes_file_path, "r", encoding="utf-8") as f:
            likes_data = json.load(f)
        with open(collections_file_path, "r", encoding="utf-8") as f:
            collections_data = json.load(f)
    except:
        return False

    # 检查笔记发布和互动
    try:
        # 查找用户发布的匹配笔记
        user_notes = [item for item in browsing_data if item.get("noteAuthor", {}).get("id") == _USER_ID and item.get("noteTitle") == _NOTE_TITLE]

        if not user_notes:
            return False

        # 获取最新匹配的笔记
        target_note = user_notes[-1]
        note_id = target_note.get("noteId")

        # 检查是否点赞
        has_liked = any(
            like.get("userId") == _USER_ID and like.get("targetId") == note_id and like.get("targetType") == "NOTE"
            for like in likes_data
        )

        # 检查是否收藏
        has_collected = any(
            col.get("userId") == _USER_ID and col.get("noteId") == note_id for col in collections_data
        )

        if has_liked and has_collected:
            return True
        else:
            return False

    except:
        return False


if __name__ == "__main__":
    print(publish_and_self_interact_check())