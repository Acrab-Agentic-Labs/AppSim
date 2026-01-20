import subprocess
import json
import os
import re

def validate_task_14(result=None, device_id=None, backup_dir=None):
    """
    任务14: 查看关注动态中所有动态的点赞数加播放量一共多少
    改进: 从APP数据源获取动态数据并计算总和
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取关注动态数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili",
                   "cat", "files/following_dynamics.json"])

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
            dynamics_file_path = os.path.join(backup_dir, 'following_dynamics.json')
            with open(dynamics_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取关注动态数据，回退验证")
            return '654335' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 关注动态数据格式错误，回退验证")
            return '654335' in final_msg

        # 3. 计算所有动态的点赞数+播放量总和
        dynamics_list = data.get("dynamics", [])
        total_sum = sum(
            dynamic.get("like_count", 0) + dynamic.get("play_count", 0)
            for dynamic in dynamics_list
        )

        # 4. 验证 final_message 中是否包含正确答案
        if str(total_sum) in final_msg:
            print(f"✓ 验证成功: 点赞数+播放量总和 = {total_sum}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={total_sum}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '654335' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '654335' in final_msg

if __name__ == '__main__':
    result = validate_task_14()
    print(result)

