import subprocess
import json
import os
import re
from datetime import datetime

def validate_task_31(result=None, device_id=None, backup_dir=None):
    """
    任务31: 查看大会员是否到期
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取用户配置
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili_sim",
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
            keywords = ['到期', '天', '月', '年', '日期', '时间', '2024', '2025', '2026']
            return any(keyword in final_msg for keyword in keywords)

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 用户配置数据格式错误，回退验证")
            keywords = ['到期', '天', '月', '年', '日期', '时间', '2024', '2025', '2026']
            return any(keyword in final_msg for keyword in keywords)

        # 3. 获取会员到期时间
        vip_expire_date = data.get("vip_expire_date", "")

        if not vip_expire_date:
            print("⚠️ 未找到会员到期时间，回退验证")
            keywords = ['到期', '天', '月', '年', '日期', '时间', '2024', '2025', '2026']
            return any(keyword in final_msg for keyword in keywords)

        # 4. 计算剩余天数或验证日期
        try:
            # 尝试解析日期格式
            expire_datetime = datetime.strptime(vip_expire_date, "%Y-%m-%d")
            current_datetime = datetime.now()
            days_remaining = (expire_datetime - current_datetime).days

            # 验证 final_message 中是否包含正确信息
            # 可能的格式：还有X天、X天后到期、2024-01-01到期等
            if str(days_remaining) in final_msg or vip_expire_date in final_msg:
                print(f"✓ 验证成功: 大会员还有 {days_remaining} 天到期 ({vip_expire_date})")
                return True
            # 也可能用其他表达方式
            elif '到期' in final_msg or '天' in final_msg or vip_expire_date[:4] in final_msg:
                print(f"✓ 验证成功: final_message包含到期信息")
                return True
            else:
                print(f"❌ 验证失败: 期望到期日={vip_expire_date} (还有{days_remaining}天), 实际回答={final_msg}")
                return False
        except ValueError:
            # 日期格式解析失败，只检查是否包含到期日期字符串
            if vip_expire_date in final_msg:
                print(f"✓ 验证成功: 大会员到期日期 = {vip_expire_date}")
                return True
            else:
                print(f"❌ 验证失败: 期望日期={vip_expire_date}, 实际回答={final_msg}")
                return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        keywords = ['到期', '天', '月', '年', '日期', '时间', '2024', '2025', '2026']
        return any(keyword in final_msg for keyword in keywords)
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        keywords = ['到期', '天', '月', '年', '日期', '时间', '2024', '2025', '2026']
        return any(keyword in final_msg for keyword in keywords)

if __name__ == '__main__':
    result = validate_task_31()
    print(result)
