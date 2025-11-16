import subprocess
import json
import sys
import io


def SearchResultCountCheck(userId="user_current", searchQuery="美妆", minCount=1, result=None, device_id=None):
    """
    检查用户搜索并统计搜索结果的笔记数目
    任务17: 在搜索栏中输入"美妆"，统计搜索结果的笔记数目
    """
    # 从设备获取搜索历史
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["exec-out", "run-as", "com.example.test05", "cat", "files/search_history.json"],
    )
    search_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 从设备获取浏览历史（用于获取笔记信息）
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["adb", "exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"],
    )
    browsing_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if search_result.returncode != 0 or not search_result.stdout:
        print(f" Failed to read search history file")
        print(f"   Reason: ADB command failed (return code: {search_result.returncode})")
        if search_result.stderr:
            print(f"   Error: {search_result.stderr}")
        return False
    if browsing_result.returncode != 0 or not browsing_result.stdout:
        print(f" Failed to read browsing history file")
        print(f"   Reason: ADB command failed (return code: {browsing_result.returncode})")
        if browsing_result.stderr:
            print(f"   Error: {browsing_result.stderr}")
        return False

    # 解析 JSON
    try:
        search_data = json.loads(search_result.stdout.strip()) if search_result.stdout.strip() else []
        browsing_data = json.loads(browsing_result.stdout.strip()) if browsing_result.stdout.strip() else []

        # 从浏览历史中提取笔记信息并构建笔记列表
        notes_data = []
        seen_note_ids = set()
        for item in browsing_data:
            note_id = item.get("noteId")
            if note_id and note_id not in seen_note_ids:
                notes_data.append(
                    {"id": note_id, "title": item.get("noteTitle", ""), "content": "", "tags": [], "topics": []}
                )
                seen_note_ids.add(note_id)
    except:
        print(f" Failed to parse JSON data")
        print(f"   Reason: Invalid JSON format")
        return False

    # 检查搜索和统计
    try:
        # 检查是否有搜索记录
        if not search_data or len(search_data) == 0:
            print(f" Search history is empty")
            print(f"   Reason: No search records found")
            print(f"   Expected: Search query '{searchQuery}'")
            return False

        # 查找用户的搜索记录
        user_searches = [
            item for item in search_data if item.get("userId") == userId and item.get("query") == searchQuery
        ]

        if not user_searches:
            print(f" Search query not found")
            print(f"   Reason: User '{userId}' did not search for '{searchQuery}'")
            recent_searches = [item.get("query", "UNKNOWN") for item in search_data if item.get("userId") == userId][:5]
            if recent_searches:
                print(f"   Recent searches: {recent_searches}")
            return False

        # 统计包含搜索关键词的笔记数量（仅通过标题匹配）
        matching_notes = [note for note in notes_data if searchQuery in note.get("title", "")]

        note_count = len(matching_notes)

        if note_count >= minCount:
            print(f"✓ Successfully searched '{searchQuery}'")
            print(f"   Found {note_count} matching notes (title matches only)")
            print(f"   Note: Content/tags/topics cannot be verified from browsing history")
            return True
        else:
            print(f" Not enough matching notes")
            print(f"   Reason: Found {note_count} notes, expected at least {minCount}")
            return False

    except:
        print(f" Error while checking search results")
        return False


if __name__ == "__main__":
    print(SearchResultCountCheck(userId="user_current", searchQuery="美妆", minCount=1))
