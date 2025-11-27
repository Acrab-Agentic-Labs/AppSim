import json
import os
import subprocess
from io import StringIO


def follow_back_fan_check(result=None, device_id=None, backup_dir=None):
    """
    检查用户是否回关了指定位置的粉丝
    任务20: 在"我"->"粉丝"对第一个粉丝进行"回关"
    """
    # 使用StringIO捕获输出，避免修改全局stdout
    output_buffer = StringIO()

    _USER_ID = "user_current"
    _AUTHOR_USERNAME = "cly_beauty"

    try:
        # 从设备获取关注列表
        message_file_path = os.path.join(backup_dir, "follows.json") if backup_dir is not None else "follows.json"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/follows.json"])

        # 将数据写入备份文件
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 检查关注列表
        try:
            if not data or len(data) == 0:
                return False

            # 查找用户是否关注了指定博主
            for follow in data:
                if (
                        follow.get("followerId") == _USER_ID
                        and follow.get("following", {}).get("username") == _AUTHOR_USERNAME
                ):
                    return True

            return False

        except:
            return False

    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(follow_back_fan_check())