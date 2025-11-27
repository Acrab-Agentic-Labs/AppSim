import json
import os
import subprocess


def set_password_check(result=None, device_id=None, backup_dir=None):
    """
    检查用户是否设置了登录密码
    任务10: 在"我"打开编辑资料右侧的设置按钮，找到"账号与安全"选项，设置登录密码为123456
    """
    _USER_ID = "user_current"
    _EXPECTED_PASSWORD = "123456"

    # 从设备获取用户数据
    message_file_path = os.path.join(backup_dir, "users.json") if backup_dir is not None else "users.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/users.json"])

    # 将数据写入备份文件
    with open(message_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return False

    # 检查密码设置
    try:
        if not data or len(data) == 0:
            return False

        # 查找当前用户
        for user in data:
            if user.get("id") == _USER_ID:
                # 检查是否设置了密码（简化处理：检查password字段）
                password = user.get("password", "")
                if password == _EXPECTED_PASSWORD:
                    return True
                else:
                    return False

        return False

    except:
        return False


if __name__ == "__main__":
    print(set_password_check())