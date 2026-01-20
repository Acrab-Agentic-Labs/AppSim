import subprocess
import json
import os
import re

def validate_task_11(result=None, device_id=None, backup_dir=None):
    """
    任务11: 在关注列表去UP主逍遥散人主页查看其粉丝数
    改进: 从APP数据源获取UP主数据
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取关注列表数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "bilibili_sim",
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
            return '23.5' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 关注列表数据格式错误，回退验证")
            return '23.5' in final_msg

        # 3. 查找逍遥散人的粉丝数
        following_list = data.get("following_list", [])
        xiaoyao_user = None
        for user in following_list:
            if "逍遥散人" in user.get("name", ""):
                xiaoyao_user = user
                break

        if not xiaoyao_user:
            print("⚠️ 未找到逍遥散人，回退验证")
            return '23.5' in final_msg

        fans_count = xiaoyao_user.get("fans_count", 0)

        # 4. 验证 final_message 中是否包含正确答案
        # 处理可能的格式：23.5万、23.5、235000等
        if str(fans_count) in final_msg or f"{fans_count:.1f}" in final_msg:
            print(f"✓ 验证成功: 逍遥散人粉丝数 = {fans_count}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={fans_count}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '23.5' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '23.5' in final_msg

if __name__ == '__main__':
    result = validate_task_11()
    print(result)
