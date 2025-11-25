import json
import subprocess


def change_nickname_check(result=None, device_id=None,backup_dir=None):
    """
    检查用户是否修改了昵称
    任务11: 在"我"打开"编辑资料"，修改自己的名字为"111"
    """
    _USER_ID = "user_current"
    _EXPECTED_NICKNAME = "111",
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

    # 检查昵称修改
    try:
        if not data or len(data) == 0:
            print(" Users list is empty")
            print("   Reason: No user records found")
            print("   Expected: At least one user record")
            return False

        # 查找当前用户
        for user in data:
            if user.get("id") == _USER_ID:
                # 检查昵称是否已修改
                nickname = user.get("nickname", "")
                if nickname == _EXPECTED_NICKNAME:
                    print("✓ Successfully changed nickname")
                    print(f"   User ID: {_USER_ID}")
                    print(f"   New nickname: {_EXPECTED_NICKNAME}")
                    return True
                else:
                    print(" Nickname does not match expected value")
                    print(f"   Reason: User nickname is '{nickname}', expected '{_EXPECTED_NICKNAME}'")
                    if not nickname:
                        print("   Note: Nickname field is empty or not set")
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
        print(" Error while checking nickname")
        return False


if __name__ == "__main__":
    print(change_nickname_check())
