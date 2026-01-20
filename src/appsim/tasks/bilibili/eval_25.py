import subprocess
import json
import os
import re

def validate_task_25(result=None, device_id=None, backup_dir=None):
    """
    任务25: 去设置里找一下uid是多少
    改进: 从APP配置中读取实际UID
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取用户配置
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili",
                   "cat", "files/user_profile.json"])

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
            profile_file_path = os.path.join(backup_dir, 'user_profile.json')
            with open(profile_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取用户配置数据，回退验证")
            return '649734343' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 用户配置数据格式错误，回退验证")
            return '649734343' in final_msg

        # 3. 获取UID
        uid = str(data.get("uid", ""))

        # 4. 验证 final_message 中是否包含正确答案
        if uid and uid in final_msg:
            print(f"✓ 验证成功: UID = {uid}")
            return True
        else:
            print(f"❌ 验证失败: 期望UID={uid}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '649734343' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '649734343' in final_msg

if __name__ == '__main__':
    result = validate_task_25()
    print(result)

