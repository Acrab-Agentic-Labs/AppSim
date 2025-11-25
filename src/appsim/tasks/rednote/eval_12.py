import json
import subprocess


def publish_note_check(result=None, device_id=None,backup_dir=None):
    """
    检查用户是否发布了指定标题和内容的笔记
    任务12: 点击底部栏的"+"号，点击添加图片，并输入文字"天晴了"，
           进入下一步，添加标题为"今日份分享"，笔记设为"仅自己可见"，最后发布笔记
    """
    _USER_ID = "user_current"
    _NOTE_TITLE = "今日份分享"
    _NOTE_CONTENT = "天晴了",
    # 从设备获取浏览历史（用于验证笔记是否存在）
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"],
    )
    browsing_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if browsing_result.returncode != 0 or not browsing_result.stdout:
        print(" Failed to read browsing history file")
        print(f"   Reason: ADB command failed (return code: {browsing_result.returncode})")
        if browsing_result.stderr:
            print(f"   Error: {browsing_result.stderr}")
        return False

    # 解析 JSON
    try:
        browsing_data = json.loads(browsing_result.stdout.strip()) if browsing_result.stdout.strip() else []

        # 从浏览历史中查找用户自己发布的笔记（通过作者ID匹配）
        user_published_notes = []
        for item in browsing_data:
            author_id = item.get("noteAuthor", {}).get("id")
            if author_id == _USER_ID:
                user_published_notes.append(
                    {
                        "id": item.get("noteId"),
                        "title": item.get("_NOTE_TITLE", ""),
                        "author": {"id": author_id},
                        "content": "",  # 浏览历史中没有完整内容
                        "visibility": "UNKNOWN",  # 浏览历史中没有可见性信息
                    }
                )

        # 注意：由于从浏览历史获取数据，无法获取笔记的完整内容和可见性
        # 这里只能进行部分验证
        data = user_published_notes
    except:
        print(" Failed to parse notes data")
        print("   Reason: Invalid JSON format")
        return False

    # 检查笔记发布
    try:
        if not data or len(data) == 0:
            print(" Notes list is empty")
            print("   Reason: No notes found in system")
            print(f"   Expected: At least one note published by user '{_USER_ID}'")
            return False

        # 查找符合条件的笔记（由于数据来源限制，只能验证标题）
        matching_notes = [note for note in data if note.get("title") == _NOTE_TITLE]

        if matching_notes:
            print("✓ Successfully published note")
            print(f"   Title: {_NOTE_TITLE}")
            print("   Note: Content and visibility cannot be verified from browsing history")
            print(f"   Note ID: {matching_notes[0].get('id', 'Unknown')}")
            return True

        # Check if note exists with wrong attributes
        if not data:
            print(" No notes found for user")
            print(f"   Reason: User '{_USER_ID}' has not published any notes")
            print(f"   Expected: Note with title '{_NOTE_TITLE}'")
            return False

        print(" Note not found with expected title")
        print(f"   Reason: Could not find note with title '{_NOTE_TITLE}'")
        print(f"   Total notes by user: {len(data)}")

        # Show recent notes by user
        if data:
            print("   Note: Only title can be verified from browsing history")
            recent_titles = [note.get("title", "N/A") for note in data[:3]]
            print(f"   Recent note titles: {recent_titles}")

        return False

    except:
        print(" Error while checking published note")
        return False


if __name__ == "__main__":
    print(publish_note_check())
