"""
功能: 检查用会议号和密码加入会议后,数据库是否正确记录参会信息
数据库位置: meetings.json, meeting_participants.json
"""

import json
import subprocess


def check_join_meeting_with_password(
    meetingId="meeting_8f4a2b", password="742983", userId="user002", result=None, device_id=None
):
    """
    检查用户是否通过正确的会议号和密码成功加入会议

    参数:
        meetingId: 会议ID(会议号)
        password: 会议密码
        userId: 加入会议的用户ID

    返回:
        bool: 如果会议存在、密码正确且用户已加入则返回True, 否则返回False
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(
            ["exec-out", "run-as", "com.example.tencentmeeting", "cat", "files/meetings.json"],
        )
        # 从Android模拟器获取meetings.json文件
        result1 = subprocess.run(
            cmd,
            stdout=open("meetings.json", "w"),
            stderr=subprocess.PIPE,
        )

        if result1.returncode != 0:
            print(f"ADB命令执行失败(meetings): {result1.stderr.decode('utf-8', errors='ignore')}")
            return False

        # 读取会议信息
        with open("meetings.json", "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print("错误: meetings.json文件为空")
                return False
            meetings = json.loads(content)

        # 验证会议是否存在且密码正确
        meeting_found = False
        for meeting in meetings:
            if meeting["meetingId"] == meetingId:
                if meeting["password"] == password:
                    meeting_found = True
                    break
                else:
                    # 密码错误
                    return False

        if not meeting_found:
            # 会议不存在
            return False

        # 从Android模拟器获取meeting_participants.json文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(
            ["exec-out", "run-as", "com.example.tencentmeeting", "cat", "files/meeting_participants.json"],
        )
        result1 = subprocess.run(cmd, stdout=open("meeting_participants.json", "w"), stderr=subprocess.PIPE)

        if result1.returncode != 0:
            print(f"ADB命令执行失败(participants): {result1.stderr.decode('utf-8', errors='ignore')}")
            return False

        # 读取参会人信息
        with open("meeting_participants.json", "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print("错误: meeting_participants.json文件为空")
                return False
            participants = json.loads(content)

        # 检查用户是否在参会人列表中
        for participant in participants:
            if participant["userId"] == userId and participant["meetingId"] == meetingId:
                return True

        # 用户未加入会议
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # 测试示例: 检查user002是否用正确密码加入了meeting_8f4a2b
    print(check_join_meeting_with_password(meetingId="meeting_8f4a2b", password="742983", userId="user002"))
