import subprocess
import json
import os
import re

def validate_task_23(result=None, device_id=None, backup_dir=None):
    """
    任务23: 查看收藏的第一个视频的视频时长
    改进: 从APP数据源获取收藏视频数据
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取收藏列表数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "bilibili_sim",
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
            return '03:45' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 收藏列表数据格式错误，回退验证")
            return '03:45' in final_msg

        # 3. 获取第一个视频的时长
        favorites_list = data.get("favorites", [])
        if not favorites_list:
            print("⚠️ 收藏列表为空，回退验证")
            return '03:45' in final_msg

        first_video = favorites_list[0]
        duration = first_video.get("duration", "")

        # 4. 验证 final_message 中是否包含正确答案
        # 处理可能的格式：03:45、3:45等
        if duration in final_msg:
            print(f"✓ 验证成功: 第一个收藏视频时长 = {duration}")
            return True
        # 也尝试去掉前导0的格式
        elif duration.startswith("0") and duration[1:] in final_msg:
            print(f"✓ 验证成功: 第一个收藏视频时长 = {duration}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={duration}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '03:45' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '03:45' in final_msg

if __name__ == '__main__':
    result = validate_task_23()
    print(result)
