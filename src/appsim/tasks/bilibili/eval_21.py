import subprocess
import json
import os
import re

def validate_task_21(result=None, device_id=None, backup_dir=None):
    """
    任务21: 看第一个视频，查看相关视频有几个
    改进: 从APP数据源获取相关视频数量，而非hardcode
    """
    # 验证 result 存在
    if result is None:
        return False

    final_msg = result.get("final_message") or ""  # final_message 可能为 None，统一按空字符串处理

    try:
        # 1. 使用 ADB 从设备拉取相关视频数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili_sim",
                   "cat", "files/related_videos.json"])

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
            related_file_path = os.path.join(backup_dir, 'related_videos.json')
            with open(related_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取相关视频数据，回退到 final_message 验证")
            # 回退到简单验证，但使用正则匹配独立数字
            pattern = r'(?:^|[^\d])4(?:[^\d]|$)'
            if re.search(pattern, final_msg):
                return True
            return False

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 相关视频数据格式错误，回退验证")
            pattern = r'(?:^|[^\d])4(?:[^\d]|$)'
            return bool(re.search(pattern, final_msg))

        # 3. 计算相关视频数量
        related_count = len(data.get("related_videos", []))

        # 4. 验证 final_message 中是否包含正确答案
        # 匹配独立的数字（避免匹配到包含该数字的其他数字）
        pattern = rf'(?:^|[^\d]){related_count}(?:[^\d]|$)'
        if re.search(pattern, final_msg):
            print(f"✓ 验证成功: 相关视频数量 = {related_count}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={related_count}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        pattern = r'(?:^|[^\d])4(?:[^\d]|$)'
        return bool(re.search(pattern, final_msg))
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        pattern = r'(?:^|[^\d])4(?:[^\d]|$)'
        return bool(re.search(pattern, final_msg))

if __name__ == '__main__':
    result = validate_task_21()
    print(result)
