import subprocess
import json
import os
import re

def validate_task_4(result=None, device_id=None, backup_dir=None):
    """
    任务4: 看一下首页罗翔老师的视频点赞加投币一共多少
    改进: 从APP数据源获取视频数据并计算点赞+投币总数
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取首页视频数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "bilibili_sim",
                   "cat", "files/home_videos.json"])

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
            home_videos_file_path = os.path.join(backup_dir, 'home_videos.json')
            with open(home_videos_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取首页视频数据，回退验证")
            return '5.1' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 首页视频数据格式错误，回退验证")
            return '5.1' in final_msg

        # 3. 查找罗翔老师的视频并计算点赞+投币数
        videos_list = data.get("videos", [])
        luoxiang_video = None
        for video in videos_list:
            if "罗翔" in video.get("author", ""):
                luoxiang_video = video
                break

        if not luoxiang_video:
            print("⚠️ 未找到罗翔老师的视频，回退验证")
            return '5.1' in final_msg

        # 计算点赞+投币总数（单位可能是万）
        like_count = luoxiang_video.get("like_count", 0)
        coin_count = luoxiang_video.get("coin_count", 0)
        total = like_count + coin_count

        # 4. 验证 final_message 中是否包含正确答案
        # 处理可能的格式：5.1万、5.1、51000等
        total_str = str(total)
        if str(total) in final_msg or f"{total:.1f}" in final_msg:
            print(f"✓ 验证成功: 点赞+投币 = {total}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={total}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '5.1' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '5.1' in final_msg

if __name__ == '__main__':
    result = validate_task_4()
    print(result)
