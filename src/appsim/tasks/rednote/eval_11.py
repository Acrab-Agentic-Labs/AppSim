import json
import os
import subprocess


def change_nickname_check(result=None, device_id=None, backup_dir=None):
    """
    检查用户是否修改了昵称
    任务11: 在"我"打开"编辑资料"，修改自己的名字为"111"
    """
    _USER_ID = "user_current"
    _EXPECTED_NICKNAME = "111"

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

    # 检查昵称修改
    try:
        if not data or len(data) == 0:
            return False

        # 查找当前用户
        for user in data:
            if user.get("id") == _USER_ID:
                # 检查昵称是否已修改
                nickname = user.get("nickname", "")
                if nickname == _EXPECTED_NICKNAME:
                    return True
                else:
                    return False

        return False

    except:
        return False


if __name__ == "__main__":
    print(change_nickname_check())