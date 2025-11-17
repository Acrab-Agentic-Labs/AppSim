import json
import subprocess


def CountAuthorNotesCheck(authorNickname="旅行日记", minCount=0, result=None, device_id=None):
    """
    检查并统计指定博主发布的笔记数量
    任务22: 统计博主"旅行日记"发布笔记数量
    """
    # 从设备获取浏览历史（用于获取笔记信息）
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    browsing_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 从设备获取用户列表
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/users.json"])
    users_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if browsing_result.returncode != 0 or not browsing_result.stdout:
        print(" Failed to read browsing history file")
        print(f"   Reason: ADB command failed (return code: {browsing_result.returncode})")
        if browsing_result.stderr:
            print(f"   Error: {browsing_result.stderr}")
        return False
    if users_result.returncode != 0 or not users_result.stdout:
        print(" Failed to read users file")
        print(f"   Reason: ADB command failed (return code: {users_result.returncode})")
        return False

    # 解析 JSON
    try:
        browsing_data = json.loads(browsing_result.stdout.strip()) if browsing_result.stdout.strip() else []
        users_data = json.loads(users_result.stdout.strip()) if users_result.stdout.strip() else []

        # 从浏览历史中提取笔记信息
        notes_data = []
        for item in browsing_data:
            author_id = item.get("noteAuthor", {}).get("id")
            notes_data.append(
                {"id": item.get("noteId"), "title": item.get("noteTitle", ""), "author": {"id": author_id}}
            )
    except:
        print(" Failed to parse JSON data")
        print("   Reason: Invalid JSON format")
        return False

    # 统计博主笔记数量
    try:
        # 查找指定昵称的博主
        target_author = None
        for user in users_data:
            if user.get("nickname") == authorNickname:
                target_author = user
                break

        if not target_author:
            print(" Author not found")
            print(f"   Reason: No user with nickname '{authorNickname}'")
            # Show available nicknames
            available_nicknames = [u.get("nickname", "UNKNOWN") for u in users_data][:10]
            print(f"   Available nicknames: {available_nicknames}")
            return False

        author_id = target_author.get("id")

        # 统计该博主的笔记数量
        author_notes = [note for note in notes_data if note.get("author", {}).get("id") == author_id]

        note_count = len(author_notes)

        if note_count >= minCount:
            print("✓ Successfully counted author notes")
            print(f"   Author: '{authorNickname}' (ID: {author_id})")
            print(f"   Total notes: {note_count}")
            return True
        else:
            print(" Not enough notes by author")
            print(f"   Author: '{authorNickname}' (ID: {author_id})")
            print(f"   Found {note_count} notes, expected at least {minCount}")
            return False

    except:
        print(" Error while counting author notes")
        return False


if __name__ == "__main__":
    print(CountAuthorNotesCheck(authorNickname="旅行日记", minCount=0))
