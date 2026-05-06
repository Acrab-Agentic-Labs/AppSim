import subprocess
import json
import os
import re

def validate_task_18(result=None, device_id=None, backup_dir=None):
    """
    任务18: 看一下接收消息通知总开关的状态
    验证逻辑: 检查返回消息中是否包含"已关闭"
    """
    if result is None:
        return False

    final_msg = result.get("final_message") or ""  # final_message 可能为 None，统一按空字符串处理

    try:
        # 1. 使用 ADB 从设备拉取设置配置
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili_sim",
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

        # 2. 验证逻辑：检查返回消息中是否包含"已关闭"
        if '已关闭' in final_msg:
            print(f"✓ 验证成功: 返回消息包含'已关闭' - {final_msg}")
            return True
        else:
            print(f"❌ 验证失败: 返回消息中未包含'已关闭' - {final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '已关闭' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '已关闭' in final_msg

if __name__ == '__main__':
    result = validate_task_18()
    print(result)
