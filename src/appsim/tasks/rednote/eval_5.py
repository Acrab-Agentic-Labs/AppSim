import json
import subprocess
from io import StringIO


def follow_author_check(result=None, device_id=None,backup_dir=None):
    # 使用StringIO捕获输出，避免修改全局stdout
    output_buffer = StringIO()
    
    _USER_ID = "user_current"
    _AUTHOR_USERNAME = "cly_beauty"
    try:
        # 设置 UTF-8 编码以支持 emoji 输出
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        """
        检查用户是否关注了指定的博主
        任务5: 在首页找到博主"小红薯美妆达人"的笔记，进入笔记并点击"关注"
        """
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
                if follow.get("followerId") == _USER_ID and follow.get("following", {}).get("username") == _AUTHOR_USERNAME:
                    # print(f"✓ Successfully followed author '{authorUsername}'")
                    return True

            # print(f"❌ Author not followed")
            # print(f"   Reason: User '{userId}' did not follow '{authorUsername}'")
            # Show current follows
            current_follows = [
                f.get("following", {}).get("username", "UNKNOWN") for f in data if f.get("followerId") == _USER_ID
            ][:5]
            # if current_follows:
            # print(f"   Current follows: {current_follows}")
            return False

        except:
            # print(f"❌ Error while checking follows")
            return False

    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(
        follow_author_check()
    )
