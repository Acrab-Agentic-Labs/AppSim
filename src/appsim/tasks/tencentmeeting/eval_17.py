"""
功能: 检查搜索手机号用户并添加好友功能
数据库位置: users.json
"""

import json
import subprocess


def check_search_user_by_phone(phone_number="15823467912", result=None, device_id=None):
    """
    通过手机号搜索用户

    参数:
        phone_number: 手机号码

    返回:
        如果找到用户返回用户信息字典, 否则返回None
    """
    # 从Android模拟器获取文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.tencentmeeting", "cat", "files/users.json"])
    result1 = subprocess.run(cmd, stdout=open("users.json", "w"), stderr=subprocess.PIPE)

    # 检查ADB命令是否成功
    if result1.returncode != 0:
        print(f"ADB命令执行失败: {result1.stderr.decode('utf-8', errors='ignore')}")
        return None

    # 读取文件
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print("错误: 文件为空,可能ADB命令未正确执行或文件在模拟器中不存在")
                return None
            data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    except FileNotFoundError:
        print("错误: 文件未找到")
        return None

    try:
        for user in data:
            if user["phone"] == phone_number:
                return {
                    "userId": user["userId"],
                    "username": user["username"],
                    "phone": user["phone"],
                    "email": user["email"],
                }
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def verify_search_result(phone_number, expected_user_id, result=None, device_id=None):
    """
    验证搜索结果是否正确

    参数:
        phone_number: 手机号码
        expected_user_id: 期望找到的用户ID

    返回:
        bool: 如果找到的用户ID匹配期望值则返回True, 否则返回False
    """
    user = check_search_user_by_phone(phone_number)
    if user and user["userId"] == expected_user_id:
        return True
    return False


if __name__ == "__main__":
    # 测试示例: 搜索手机号15823467912
    user = check_search_user_by_phone("15823467912")
    if user:
        print(f"找到用户: {user['username']}, ID: {user['userId']}")
    else:
        print("未找到用户")
