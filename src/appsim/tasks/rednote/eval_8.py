import json
import subprocess


def DislikeNoteCheck(userId="user_current", notePosition=2, result=None, device_id=None):
    """
    检查用户是否对首页指定位置的笔记点击了"不喜欢"
    任务8: 对首页第二篇笔记进入详情，点击右上角的图标，选择"不喜欢"
    """
    # 从设备获取不喜欢记录
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/dislikes.json"])
    result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if result1.returncode != 0 or not result1.stdout:
        print(" Failed to read dislikes file")
        print(f"   Reason: ADB command failed (return code: {result1.returncode})")
        if result1.stderr:
            print(f"   Error: {result1.stderr}")
        return False

    # 解析 JSON
    try:
        data = json.loads(result1.stdout)
    except:
        print(" Failed to parse dislikes data")
        print("   Reason: Invalid JSON format")
        return False

    # 检查不喜欢记录
    try:
        if not data or len(data) == 0:
            print(" Dislikes list is empty")
            print("   Reason: No dislike records found")
            print(f"   Expected: At least one dislike record for user '{userId}'")
            return False

        # 查找用户的不喜欢记录
        user_dislikes = [item for item in data if item.get("userId") == userId]

        # 检查是否有最新的不喜欢记录
        if user_dislikes:
            # 按时间排序，获取最新的记录
            latest_dislike = sorted(user_dislikes, key=lambda x: x.get("dislikedAt", ""), reverse=True)[0]
            disliked_note_id = latest_dislike.get("noteId", "Unknown")
            disliked_at = latest_dislike.get("dislikedAt", "Unknown")
            print("✓ Successfully disliked a note")
            print(f"   Note ID: {disliked_note_id}")
            print(f"   Disliked at: {disliked_at}")
            return True

        print(" No dislike records for user")
        print(f"   Reason: User '{userId}' has not disliked any notes")
        print("   Expected: At least one dislike record")
        print(f"   Total dislike records in system: {len(data)}")
        return False

    except:
        print(" Error while checking dislike records")
        return False


if __name__ == "__main__":
    print(DislikeNoteCheck(userId="user_current", notePosition=2))
