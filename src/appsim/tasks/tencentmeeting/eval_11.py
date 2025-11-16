"""
功能: 检查开启手机屏幕共享后,数据库是否正确记录
数据库位置: meeting_participants.json
"""

import json
import subprocess


def check_screen_sharing(
    userId="user002", meetingId="meeting_3d7e91", expected_sharing_status=True, result=None, device_id=None
):
    """
    检查指定用户在指定会议中的屏幕共享状态

    参数:
        userId: 用户ID
        meetingId: 会议ID
        expected_sharing_status: 期望的屏幕共享状态 (True表示正在共享, False表示未共享)

    返回:
        bool: 如果实际状态与期望状态匹配则返回True, 否则返回False
    """
    # 从Android模拟器获取文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["exec-out", "run-as", "com.example.tencentmeeting", "cat", "files/meeting_participants.json"],
    )
    result1 = subprocess.run(cmd, stdout=open("meeting_participants.json", "w"), stderr=subprocess.PIPE)

    # 检查ADB命令是否成功
    if result1.returncode != 0:
        print(f"ADB命令执行失败: {result1.stderr.decode('utf-8', errors='ignore')}")
        return False

    # 读取文件
    try:
        with open("meeting_participants.json", "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print("错误: 文件为空,可能ADB命令未正确执行或文件在模拟器中不存在")
                return False
            data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return False
    except FileNotFoundError:
        print("错误: 文件未找到")
        return False

    # 查找匹配的用户和会议记录
    try:
        for participant in data:
            if participant["userId"] == userId and participant["meetingId"] == meetingId:
                # 检查isSharingScreen字段是否与期望状态匹配
                if participant["isSharingScreen"] == expected_sharing_status:
                    return True
                else:
                    return False
        # 如果没有找到匹配的记录
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # 测试示例: 检查user002在meeting_3d7e91中是否正在共享屏幕
    print(
        check_screen_sharing(
            userId="user002",
            meetingId="meeting_3d7e91",
            expected_sharing_status=True,  # 期望正在共享屏幕
        )
    )
