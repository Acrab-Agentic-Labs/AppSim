import json
import subprocess


def set_password_check(result=None, device_id=None,backup_dir=None):
    """
    检查用户是否设置了登录密码
    任务10: 在"我"打开编辑资料右侧的设置按钮，找到"账号与安全"选项，设置登录密码为123456
    """
    _USER_ID = "user_current"
    _EXPECTED_PASSWORD = "123456",
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
        print(" Failed to read users file")
        print(f"   Reason: ADB command failed (return code: {result1.returncode})")
        if result1.stderr:
            print(f"   Error: {result1.stderr}")
        return False

    # 解析 JSON
    try:
        data = json.loads(result1.stdout)
    except:
        print(" Failed to parse users data")
        print("   Reason: Invalid JSON format")
        return False

    # 检查密码设置
    try:
        if not data or len(data) == 0:
            print(" Users list is empty")
            print("   Reason: No user records found")
            print("   Expected: At least one user record")
            return False

        # 查找当前用户
        for user in data:
            if user.get("id") == _USER_ID:
                # 检查是否设置了密码（简化处理：检查password字段）
                password = user.get("password", "")
                if password == _EXPECTED_PASSWORD:
                    print("✓ Successfully set password")
                    print(f"   User ID: {_USER_ID}")
                    print(f"   Password: {_EXPECTED_PASSWORD}")
                    return True
                else:
                    print(" Password does not match expected value")
                    print(f"   Reason: User password is '{password}', expected '{_EXPECTED_PASSWORD}'")
                    if not password:
                        print("   Note: Password field is empty or not set")
                    return False

        print(" User not found")
        print(f"   Reason: User '{_USER_ID}' does not exist in users list")
        print(f"   Total users in system: {len(data)}")
        # Show available user IDs
        _USER_IDs = [user.get("id", "Unknown") for user in data[:5]]
        if _USER_IDs:
            print(f"   Available user IDs (first 5): {_USER_IDs}")
        return False

    except:
        print(" Error while checking password")
        return False


if __name__ == "__main__":
    print(set_password_check())
