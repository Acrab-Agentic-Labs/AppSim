import json
import subprocess


def ViewAndCommentNotesCheck(result=None, device_id=None):
    """
    检查浏览历史和评论记录的最后三条数据：
    1. browsing_history.json 最后三条: noteId 分别为 note_010, note_011, note_012
    2. comments.json 最后三条: content 均为 "很实用！", noteId 分别为 note_010, note_011, note_012
    """

    # 检查浏览历史
    print("=== Checking browsing_history.json ===")
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    browsing_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    if browsing_result.returncode != 0 or not browsing_result.stdout:
        print(" Failed to read browsing_history.json")
        print(f"   Reason: ADB command failed (return code: {browsing_result.returncode})")
        return False

    try:
        browsing_data = json.loads(browsing_result.stdout)
        if not browsing_data or len(browsing_data) < 3:
            print(" Browsing history has less than 3 records")
            print(f"   Found: {len(browsing_data) if browsing_data else 0} records")
            print("   Expected: At least 3 records")
            return False

        # 获取最后三条浏览历史
        last_three_browsing = browsing_data[-3:]
        browsing_note_ids = [item.get("noteId", "") for item in last_three_browsing]

        expected_browsing_ids = ["note_010", "note_011", "note_012"]

        if browsing_note_ids == expected_browsing_ids:
            print("✓ Browsing history check passed")
            for i, item in enumerate(last_three_browsing):
                print(f"   Record {i + 1}:")
                print(f"     Note ID: {item.get('noteId')}")
                print(f"     Note Title: {item.get('noteTitle', 'Unknown')}")
                print(f"     Browsed at: {item.get('browsedAt', 'Unknown')}")
        else:
            print(" Browsing history check failed")
            print(f"   Expected note IDs: {expected_browsing_ids}")
            print(f"   Actual note IDs: {browsing_note_ids}")
            return False
    except:
        return False

    # 检查评论记录
    print("\n=== Checking comments.json ===")
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/comments.json"])
    comments_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    if comments_result.returncode != 0 or not comments_result.stdout:
        print(" Failed to read comments.json")
        print(f"   Reason: ADB command failed (return code: {comments_result.returncode})")
        return False

    try:
        comments_data = json.loads(comments_result.stdout)
        if not comments_data or len(comments_data) < 3:
            print(" Comments list has less than 3 records")
            print(f"   Found: {len(comments_data) if comments_data else 0} records")
            print("   Expected: At least 3 records")
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
                print(f" Comment {i + 1} check failed")
                print(f"   Expected: content='{expected_content}', noteId='{expected_note_id}'")
                print(f"   Actual: content='{content}', noteId='{note_id}'")

        if all_match:
            print("✓ Comments check passed")
            for i, comment in enumerate(last_three_comments):
                print(f"   Comment {i + 1}:")
                print(f"     Content: {comment.get('content')}")
                print(f"     Note ID: {comment.get('noteId')}")
                print(f"     Created at: {comment.get('createdAt', 'Unknown')}")
        else:
            return False

    except:
        return False

    # 所有检查都通过
    print("\n" + "=" * 50)
    print("✓ All checks passed!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    print(ViewAndCommentNotesCheck())
