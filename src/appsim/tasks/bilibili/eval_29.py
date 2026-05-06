import subprocess
import json
import os
import re

def validate_task_29(result=None, device_id=None, backup_dir=None):
    """
    任务29: 在直播推荐页面，查看直播人数最少的两个的在线观看人数一共多少
    改进: 从APP数据源获取直播列表并计算人数最少的两个的总和
    """
    if result is None:
        return False

    final_msg = result.get("final_message") or ""  # final_message 可能为 None，统一按空字符串处理

    try:
        # 1. 使用 ADB 从设备拉取直播推荐数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili_sim",
                   "cat", "files/live_streams.json"])

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
            live_file_path = os.path.join(backup_dir, 'live_streams.json')
            with open(live_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取直播推荐数据，回退验证")
            return '8623' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 直播推荐数据格式错误，回退验证")
            return '8623' in final_msg

        # 3. 找出人数最少的两个直播间并计算总和
        live_streams = data.get("live_streams", [])
        if len(live_streams) < 2:
            print(f"⚠️ 直播数量不足2个（当前{len(live_streams)}个），回退验证")
            return '8623' in final_msg

        # 按在线人数排序，取最小的两个
        sorted_streams = sorted(live_streams, key=lambda x: x.get("viewer_count", 0))
        total_viewers = sum(stream.get("viewer_count", 0) for stream in sorted_streams[:2])

        # 4. 验证 final_message 中是否包含正确答案
        if str(total_viewers) in final_msg:
            print(f"✓ 验证成功: 人数最少的两个直播间总观看人数 = {total_viewers}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={total_viewers}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '8623' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '8623' in final_msg

if __name__ == '__main__':
    result = validate_task_29()
    print(result)
