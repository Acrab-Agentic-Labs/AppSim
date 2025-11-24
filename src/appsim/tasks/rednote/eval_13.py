import subprocess
import json
import sys
import io
import os
from io import StringIO


def ShareNoteCheck(userId,result=None, device_id=None,backup_dir=None):
    """
    检查用户是否分享了首页第一篇笔记
    任务13: 在首页第一篇笔记详情页点击右上角"分享"按钮
    """
    # 使用StringIO捕获输出，避免修改全局stdout
    output_buffer = StringIO()
    # 从设备获取分享记录
    message_file_path = os.path.join(backup_dir, 'shares.json') if backup_dir else 'shares.json'
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.test05', 'cat', 'files/shares.json'])
    result1 = subprocess.run(
        cmd,
        capture_output=True,
        encoding='utf-8',
        errors='replace'
    )
    # try:
    #     with open(message_file_path, "r",encoding='utf-8') as f:
    #         data = json.load(f)
    #         if isinstance(data, list):
    #             data = data[-1] if data else {}
    # except :
    #     return False

    # 检查命令是否成功执行
    if result1.returncode != 0 or not result1.stdout:
        print(f" Failed to read shares file")
        print(f"   Reason: ADB command failed (return code: {result1.returncode})")
        if result1.stderr:
            print(f"   Error: {result1.stderr}")
        return False

    # 解析 JSON
    try:
        data = json.loads(result1.stdout)
    except (json.JSONDecodeError, TypeError) as e:
        print(f" Failed to parse shares data")
        print(f"   Reason: Invalid JSON format")
        print(f"   Error: {e}")
        return False

    # 检查分享记录
    try:
        if not data or len(data) == 0:
            print(f" Shares list is empty")
            print(f"   Reason: No share records found")
            print(f"   Expected: At least one share record for user '{userId}'")
            return False

        # 查找用户的分享记录
        user_shares = [item for item in data if item.get('userId') == userId]

        # 如果有最新的分享记录，返回 True
        if user_shares:
            # 按时间排序，获取最新的分享
            latest_share = sorted(user_shares, key=lambda x: x.get('sharedAt', ''), reverse=True)[0]
            shared_note_id = latest_share.get('noteId', 'Unknown')
            shared_at = latest_share.get('sharedAt', 'Unknown')
            print(f"Successfully shared a note")
            print(f"   Note ID: {shared_note_id}")
            print(f"   Shared at: {shared_at}")
            return True

        print(f" No share records for user")
        print(f"   Reason: User '{userId}' has not shared any notes")
        print(f"   Expected: At least one share record")
        print(f"   Total share records in system: {len(data)}")
        return False

    except Exception as e:
        print(f" Error while checking share records")
        print(f"   Reason: {e}")
        return False

    finally:
        # 释放缓冲区资源
        output_buffer.close()

if __name__ == "__main__":
    print(ShareNoteCheck(
        userId='user_current'
    ))
