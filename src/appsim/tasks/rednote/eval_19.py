import subprocess
import json
import sys
import io


def NoteInteractionCheck(result=None, device_id=None):
    """
    检查三个文件的最后一条记录是否符合条件：
    1. browsing_history.json: noteAuthor.id = "user_003", noteTitle = "AI技术在日常生活中的应用，太实用了！"
    2. likes.json: targetId = "note_002"
    3. comments.json: content = "很实用！", noteId = "note_002"
    """

    # 检查浏览历史
    print("=== Checking browsing_history.json ===")
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    browsing_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    if browsing_result.returncode != 0 or not browsing_result.stdout:
        print(f" Failed to read browsing_history.json")
        print(f"   Reason: ADB command failed (return code: {browsing_result.returncode})")
        return False

    try:
        browsing_data = json.loads(browsing_result.stdout)
        if not browsing_data or len(browsing_data) == 0:
            print(f" Browsing history is empty")
            return False

        last_browsing = browsing_data[-1]
        browsing_author_id = last_browsing.get("noteAuthor", {}).get("id", "")
        browsing_title = last_browsing.get("noteTitle", "")

        if browsing_author_id == "user_003" and browsing_title == "AI技术在日常生活中的应用，太实用了！":
            print(f"✓ Browsing history check passed")
            print(f"   Note Author ID: {browsing_author_id}")
            print(f"   Note Title: {browsing_title}")
            print(f"   Browsed at: {last_browsing.get('browsedAt', 'Unknown')}")
        else:
            print(f" Browsing history check failed")
            print(f"   Expected: noteAuthor.id='user_003', noteTitle='AI技术在日常生活中的应用，太实用了！'")
            print(f"   Actual: noteAuthor.id='{browsing_author_id}', noteTitle='{browsing_title}'")
            return False
    except:
        return False

    # 检查点赞记录
    print("\n=== Checking likes.json ===")
    likes_result = subprocess.run(
        ["exec-out", "run-as", "com.example.test05", "cat", "files/likes.json"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if likes_result.returncode != 0 or not likes_result.stdout:
        print(f" Failed to read likes.json")
        print(f"   Reason: ADB command failed (return code: {likes_result.returncode})")
        return False

    try:
        likes_data = json.loads(likes_result.stdout)
        if not likes_data or len(likes_data) == 0:
            print(f" Likes list is empty")
            return False

        last_like = likes_data[-1]
        like_target_id = last_like.get("targetId", "")

        if like_target_id == "note_002":
            print(f"✓ Like check passed")
            print(f"   Target ID: {like_target_id}")
            print(f"   Liked at: {last_like.get('likedAt', 'Unknown')}")
        else:
            print(f" Like check failed")
            print(f"   Expected: targetId='note_002'")
            print(f"   Actual: targetId='{like_target_id}'")
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
        print(f" Failed to read comments.json")
        print(f"   Reason: ADB command failed (return code: {comments_result.returncode})")
        return False

    try:
        comments_data = json.loads(comments_result.stdout)
        if not comments_data or len(comments_data) == 0:
            print(f" Comments list is empty")
            return False

        last_comment = comments_data[-1]
        comment_content = last_comment.get("content", "")
        comment_note_id = last_comment.get("noteId", "")

        if comment_content == "很实用！" and comment_note_id == "note_002":
            print(f"✓ Comment check passed")
            print(f"   Content: {comment_content}")
            print(f"   Note ID: {comment_note_id}")
            print(f"   Created at: {last_comment.get('createdAt', 'Unknown')}")
        else:
            print(f" Comment check failed")
            print(f"   Expected: content='很实用！', noteId='note_002'")
            print(f"   Actual: content='{comment_content}', noteId='{comment_note_id}'")
            return False
    except:
        return False

    # 所有检查都通过
    print("\n" + "=" * 50)
    print("✓ All checks passed!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    print(NoteInteractionCheck())
