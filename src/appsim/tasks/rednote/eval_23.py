# eval_23.py
import json
import os
import subprocess
from io import StringIO


def verify_author_unfollowed(result=None, device_id=None, backup_dir=None):
    output_buffer = StringIO()

    _USER_ID = "user_current"
    _AUTHOR_USERNAME = "fashion_girl"

    try:
        # 从设备获取关注列表
        message_file_path = os.path.join(backup_dir, "follows.json") if backup_dir is not None else "follows.json"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/follows.json"])

        # 将数据写入备份文件
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        try:
            with open(message_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        if not data or len(data) == 0:
            return True

        # 查找用户是否关注了指定博主
        for follow in data:
            if (
                    follow.get("followerId") == _USER_ID
                    and follow.get("following", {}).get("username") == _AUTHOR_USERNAME
            ):
                return False

        return True

    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(verify_author_unfollowed())