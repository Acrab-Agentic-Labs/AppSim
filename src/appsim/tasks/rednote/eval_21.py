import json
import os
import subprocess


def view_and_comment_notes_check(result=None, device_id=None, backup_dir=None):
    """
    检查浏览历史和评论记录的最后三条数据：
    1. browsing_history.json 最后三条: noteId 分别为 note_010, note_011, note_012
    2. comments.json 最后三条: content 均为 "很实用！", noteId 分别为 note_010, note_011, note_012
    """
    # 检查浏览历史
    browsing_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    with open(browsing_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(browsing_file_path, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)
        if not browsing_data or len(browsing_data) < 3:
            return False

        # 获取最后三条浏览历史
        last_three_browsing = browsing_data[-3:]
        browsing_note_ids = [item.get("noteId", "") for item in last_three_browsing]
        expected_browsing_ids = ["note_010", "note_011", "note_012"]

        if browsing_note_ids != expected_browsing_ids:
            return False
    except:
        return False

    # 检查评论记录
    comments_file_path = os.path.join(backup_dir, "comments.json") if backup_dir is not None else "comments.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/comments.json"])
    with open(comments_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(comments_file_path, "r", encoding="utf-8") as f:
            comments_data = json.load(f)
        if not comments_data or len(comments_data) < 3:
            return False

        # 获取最后三条评论
        last_three_comments = comments_data[-3:]

        # 检查每条评论的 content 和 noteId
        expected_content = "很实用！"
        expected_note_ids = ["note_010", "note_011", "note_012"]

        all_match = True
        for i, comment in enumerate(last_three_comments):
            content = comment.get("content", "")
            note_id = comment.get("noteId", "")
            expected_note_id = expected_note_ids[i]

            if content != expected_content or note_id != expected_note_id:
                all_match = False
                break

        if not all_match:
            return False

    except:
        return False

    # 所有检查都通过
    return True


if __name__ == "__main__":
    print(view_and_comment_notes_check())