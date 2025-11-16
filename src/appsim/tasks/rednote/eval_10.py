import subprocess
import json
import sys
import io


def SetPasswordCheck(userId="user_current", expectedPassword="123456", result=None, device_id=None):
    """
    检查用户是否设置了登录密码
    任务10: 在"我"打开编辑资料右侧的设置按钮，找到"账号与安全"选项，设置登录密码为123456
    """
    # 从设备获取用户数据
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["exec-out", "run-as", "com.example.test05", "cat", "files/users.json"],
    )
    result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if result1.returncode != 0 or not result1.stdout:
        print(f" Failed to read users file")
        print(f"   Reason: ADB command failed (return code: {result1.returncode})")
        if result1.stderr:
            print(f"   Error: {result1.stderr}")
        return False

    # 解析 JSON
    try:
        data = json.loads(result1.stdout)
    except:
        print(f" Failed to parse users data")
        print(f"   Reason: Invalid JSON format")
        return False

    # 检查密码设置
    try:
        if not data or len(data) == 0:
            print(f" Users list is empty")
            print(f"   Reason: No user records found")
            print(f"   Expected: At least one user record")
            return False

        # 查找当前用户
        for user in data:
            if user.get("id") == userId:
                # 检查是否设置了密码（简化处理：检查password字段）
                password = user.get("password", "")
                if password == expectedPassword:
                    print(f"✓ Successfully set password")
                    print(f"   User ID: {userId}")
                    print(f"   Password: {expectedPassword}")
                    return True
                else:
                    print(f" Password does not match expected value")
                    print(f"   Reason: User password is '{password}', expected '{expectedPassword}'")
                    if not password:
                        print(f"   Note: Password field is empty or not set")
                    return False

        print(f" User not found")
        print(f"   Reason: User '{userId}' does not exist in users list")
        print(f"   Total users in system: {len(data)}")
        # Show available user IDs
        user_ids = [user.get("id", "Unknown") for user in data[:5]]
        if user_ids:
            print(f"   Available user IDs (first 5): {user_ids}")
        return False

    except:
        print(f" Error while checking password")
        return False


if __name__ == "__main__":
    print(SetPasswordCheck(userId="user_current", expectedPassword="123456"))
