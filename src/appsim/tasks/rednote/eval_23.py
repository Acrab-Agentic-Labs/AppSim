import json
import subprocess
from io import StringIO


def UnfollowAuthorCheck(userId="user_current", authorUsername="fashion_girl", result=None, device_id=None):
    """
    检查用户是否取消关注了指定博主
    任务23: 在我的关注列表对"潮流时尚达人"取消关注
    """
    # 使用StringIO捕获输出，避免修改全局stdout
    output_buffer = StringIO()

    try:
        # 从设备获取关注列表
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/follows.json"])

        result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

        # 检查命令是否成功执行
        if result1.returncode != 0 or not result1.stdout:
            # print(f"❌ Failed to read follows file")
            # print(f"   Reason: ADB command failed (return code: {result1.returncode})")
            # if result1.stderr:
            # print(f"   Error: {result1.stderr}")
            return False

        # 解析 JSON
        try:
            data = json.loads(result1.stdout)
        except:
            # print(f"❌ Failed to parse follows data")
            # print(f"   Reason: Invalid JSON format")
            return False

        # 检查关注列表
        try:
            if not data or len(data) == 0:
                # print(f"❌ Follows list is empty")
                # print(f"   Reason: No follow records found")
                # print(f"   Expected: Following '{authorUsername}'")
                return False

            # 查找用户是否关注了指定博主
            for follow in data:
                if follow.get("followerId") == userId and follow.get("following", {}).get("username") == authorUsername:
                    # print(f"✓ Successfully followed author '{authorUsername}'")
                    return False

            # print(f"❌ Author not followed")
            # print(f"   Reason: User '{userId}' did not follow '{authorUsername}'")
            # if current_follows:
            # print(f"   Current follows: {current_follows}")
            return True

        except:
            # print(f"❌ Error while checking follows")
            return False

    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(UnfollowAuthorCheck(userId="user_current", authorUsername="fashion_girl"))
