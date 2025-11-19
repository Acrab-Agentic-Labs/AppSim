import json
import subprocess


def PublishAndSelfInteractCheck(
    userId="user_current",
    noteTitle="今日分享",
    noteContent="今天也要加油呀",
    visibility="PUBLIC",
    result=None,
    device_id=None,
):
    """
    检查用户是否发布了指定笔记并对其进行点赞和收藏
    任务18: 点击底部栏的"+"号，点击添加图片，并输入文字"今天也要加油呀"，
           进入下一步，添加标题为"今日分享"，笔记设为"公开可见"，最后发布笔记并对这篇笔记进行点赞、收藏
    """
    # 从设备获取浏览历史（用于验证笔记）
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    browsing_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 从设备获取点赞记录
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/likes.json"])
    likes_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 从设备获取收藏记录
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/collections.json"])
    collections_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if browsing_result.returncode != 0 or not browsing_result.stdout:
        print(" Failed to read browsing history file")
        print(f"   Reason: ADB command failed (return code: {browsing_result.returncode})")
        if browsing_result.stderr:
            print(f"   Error: {browsing_result.stderr}")
        return False
    if likes_result.returncode != 0:
        print(" Failed to read likes file")
        print(f"   Reason: ADB command failed (return code: {likes_result.returncode})")
        return False
    if collections_result.returncode != 0:
        print(" Failed to read collections file")
        print(f"   Reason: ADB command failed (return code: {collections_result.returncode})")
        return False

    # 解析 JSON
    try:
        browsing_data = json.loads(browsing_result.stdout.strip()) if browsing_result.stdout.strip() else []
        likes_data = json.loads(likes_result.stdout.strip()) if likes_result.stdout.strip() else []
        collections_data = json.loads(collections_result.stdout.strip()) if collections_result.stdout.strip() else []

        # 从浏览历史中提取用户发布的笔记
        notes_data = []
        for item in browsing_data:
            author_id = item.get("noteAuthor", {}).get("id")
            if author_id == userId:
                notes_data.append(
                    {
                        "id": item.get("noteId"),
                        "title": item.get("noteTitle", ""),
                        "content": "",  # 浏览历史中没有完整内容
                        "visibility": "UNKNOWN",  # 浏览历史中没有可见性信息
                        "author": {"id": author_id},
                    }
                )
    except:
        print(" Failed to parse JSON data")
        print("   Reason: Invalid JSON format")
        return False

    # 检查笔记发布和互动
    try:
        # 查找用户发布的匹配笔记（仅通过标题匹配，无法验证内容和可见性）
        user_notes = [note for note in notes_data if note.get("title") == noteTitle]

        if not user_notes:
            print(" Published note not found")
            print(f"   Expected: Title='{noteTitle}'")
            print("   Note: Content and visibility cannot be verified from browsing history")
            # Show recent notes by user
            if notes_data:
                recent_titles = [n.get("title", "N/A") for n in notes_data[:3]]
                print(f"   Recent note titles by user: {recent_titles}")
            return False

        # 获取最新匹配的笔记
        target_note = user_notes[-1]  # 假设最后一个是最新的
        note_id = target_note.get("id")

        # 检查是否点赞
        has_liked = any(
            like.get("userId") == userId and like.get("targetId") == note_id and like.get("targetType") == "NOTE"
            for like in likes_data
        )

        # 检查是否收藏
        has_collected = any(col.get("userId") == userId and col.get("noteId") == note_id for col in collections_data)

        if has_liked and has_collected:
            print("✓ Successfully published and interacted with note")
            print(f"   Note ID: {note_id}")
            print(f"   Title: '{noteTitle}'")
            print("   Liked: ✓, Collected: ✓")
            print("   Note: Content and visibility cannot be verified from browsing history")
            return True
        else:
            print(" Note published but missing interactions")
            print(f"   Note ID: {note_id}")
            print(f"   Title: '{noteTitle}'")
            print(f"   Liked: {'✓' if has_liked else '✗'}")
            print(f"   Collected: {'✓' if has_collected else '✗'}")
            return False

    except:
        print(" Error while checking published note")
        return False


if __name__ == "__main__":
    print(
        PublishAndSelfInteractCheck(
            userId="user_current", noteTitle="今日分享", noteContent="今天也要加油呀", visibility="PUBLIC"
        )
    )
