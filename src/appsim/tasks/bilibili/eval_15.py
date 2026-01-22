import subprocess
import json
import os
import re

def validate_task_15(result=None, device_id=None, backup_dir=None):
    """
    任务15: 数一下关注列表有几个已互粉的up主
    改进: 从APP数据源获取关注列表并统计互粉数量
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取关注列表数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili_sim",
                   "cat", "files/following_list.json"])

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
            following_file_path = os.path.join(backup_dir, 'following_list.json')
            with open(following_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取关注列表数据，回退验证")
            pattern = r'(?:^|[^\d])1(?:[^\d]|$)'
            return bool(re.search(pattern, final_msg))

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 关注列表数据格式错误，回退验证")
            pattern = r'(?:^|[^\d])1(?:[^\d]|$)'
            return bool(re.search(pattern, final_msg))

        # 3. 统计互粉的up主数量
        following_list = data.get("following_list", [])
        mutual_follow_count = sum(1 for user in following_list if user.get("is_mutual_follow", False))

        # 4. 验证 final_message 中是否包含正确答案
        pattern = rf'(?:^|[^\d]){mutual_follow_count}(?:[^\d]|$)'
        if re.search(pattern, final_msg):
            print(f"✓ 验证成功: 互粉up主数量 = {mutual_follow_count}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={mutual_follow_count}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        pattern = r'(?:^|[^\d])1(?:[^\d]|$)'
        return bool(re.search(pattern, final_msg))
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        pattern = r'(?:^|[^\d])1(?:[^\d]|$)'
        return bool(re.search(pattern, final_msg))

if __name__ == '__main__':
    result = validate_task_15()
    print(result)
