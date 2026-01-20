import subprocess
import json
import os
import re

def validate_task_24(result=None, device_id=None, backup_dir=None):
    """
    任务24: 在收藏页面查看该收藏中共收藏了多少个视频
    改进: 从APP数据源获取收藏列表并统计数量
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取收藏列表数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili",
                   "cat", "files/favorites.json"])

        result_data = subprocess.run(
            cmd,
            capture_output=True,
            encoding='utf-8',
            errors='replace',
            text=True,
            timeout=10
        )

        # 保存数据到备份目录
        if backup_dir:
            favorites_file_path = os.path.join(backup_dir, 'favorites.json')
            with open(favorites_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取收藏列表数据，回退验证")
            pattern = r'\b10\b'
            return bool(re.search(pattern, final_msg))

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 收藏列表数据格式错误，回退验证")
            pattern = r'\b10\b'
            return bool(re.search(pattern, final_msg))

        # 3. 统计收藏视频数量
        favorites_list = data.get("favorites", [])
        favorites_count = len(favorites_list)

        # 4. 验证 final_message 中是否包含正确答案
        pattern = rf'\b{favorites_count}\b'
        if re.search(pattern, final_msg):
            print(f"✓ 验证成功: 收藏视频数量 = {favorites_count}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={favorites_count}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        pattern = r'\b10\b'
        return bool(re.search(pattern, final_msg))
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        pattern = r'\b10\b'
        return bool(re.search(pattern, final_msg))

if __name__ == '__main__':
    result = validate_task_24()
    print(result)
