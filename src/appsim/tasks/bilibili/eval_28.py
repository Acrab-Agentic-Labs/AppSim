import subprocess
import json
import os
import re

def validate_task_28(result=None, device_id=None, backup_dir=None):
    """
    任务28: 在设置中，查看当前定时关闭状态
    改进: 从APP配置中读取实际状态
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取设置配置
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "bilibili_sim",
                   "cat", "files/settings.json"])

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
            settings_file_path = os.path.join(backup_dir, 'settings.json')
            with open(settings_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取设置数据，回退验证")
            return '不开启' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 设置数据格式错误，回退验证")
            return '不开启' in final_msg

        # 3. 获取定时关闭状态
        timer_close_enabled = data.get("timer_close_enabled", False)
        timer_close_time = data.get("timer_close_time", "")

        # 4. 验证 final_message 中是否包含正确答案
        if timer_close_enabled:
            # 如果开启，应该包含时间信息
            expected_keywords = ["开启", "已开启", "启用"]
            # 也可能包含具体时间
            if timer_close_time and timer_close_time in final_msg:
                print(f"✓ 验证成功: 定时关闭状态 = 已开启 ({timer_close_time})")
                return True
            elif any(keyword in final_msg for keyword in expected_keywords):
                print(f"✓ 验证成功: 定时关闭状态 = 已开启")
                return True
        else:
            # 如果关闭，应该包含关闭相关信息
            expected_keywords = ["不开启", "未开启", "关闭", "已关闭", "未启用", "禁用"]
            if any(keyword in final_msg for keyword in expected_keywords):
                print(f"✓ 验证成功: 定时关闭状态 = 不开启")
                return True

        print(f"❌ 验证失败: 期望状态={'开启' if timer_close_enabled else '不开启'}, 实际回答={final_msg}")
        return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '不开启' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '不开启' in final_msg

if __name__ == '__main__':
    result = validate_task_28()
    print(result)
