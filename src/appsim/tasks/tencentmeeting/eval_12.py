"""
功能: 检查举手申请发言后,数据库是否正确记录
数据库位置: meeting_participants.json, hand_raise_records.json
"""

import json
import subprocess


def check_hand_raise(userId="user003", meetingId="meeting_3d7e91", result=None, device_id=None):
    """
    检查用户是否举手申请发言

    参数:
        userId: 用户ID
        meetingId: 会议ID

    返回:
        bool: 如果用户已举手则返回True, 否则返回False
    """
    try:
        # 从Android模拟器获取meeting_participants.json文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.tencentmeeting", "cat", "files/meeting_participants.json"])
        result1 = subprocess.run(cmd, stdout=open("meeting_participants.json", "w"), stderr=subprocess.PIPE)

        if result1.returncode != 0:
            print(f"ADB命令执行失败(participants): {result1.stderr.decode('utf-8', errors='ignore')}")
            return False

        # 检查meeting_participants中的举手状态
        with open("meeting_participants.json", "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print("错误: meeting_participants.json文件为空")
                return False
            participants = json.loads(content)

        participant_raised = False
        for participant in participants:
            if participant["userId"] == userId and participant["meetingId"] == meetingId:
                if participant["isHandRaised"]:
                    participant_raised = True
                    break

        # 从Android模拟器获取hand_raise_records.json文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.tencentmeeting", "cat", "files/hand_raise_records.json"])
        result1 = subprocess.run(cmd, stdout=open("hand_raise_records.json", "w"), stderr=subprocess.PIPE)

        if result1.returncode != 0:
            print(f"ADB命令执行失败(hand_raise): {result1.stderr.decode('utf-8', errors='ignore')}")
            return False

        # 检查hand_raise_records中是否有记录
        with open("hand_raise_records.json", "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print("错误: hand_raise_records.json文件为空")
                return False
            records = json.loads(content)

        record_exists = False
        for record in records:
            if (
                record["userId"] == userId and record["meetingId"] == meetingId and record["lowerTime"] is None
            ):  # 还未放下手
                record_exists = True
                break

        # 两个数据源都确认举手状态
        return participant_raised and record_exists

    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # 测试示例: 检查user003在meeting_3d7e91中是否举手
    print(check_hand_raise(userId="user003", meetingId="meeting_3d7e91"))
