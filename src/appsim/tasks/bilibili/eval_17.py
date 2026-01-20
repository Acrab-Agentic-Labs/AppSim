import subprocess
import json
import os
import re

def validate_task_17(result=None, device_id=None, backup_dir=None):
    """
    任务17: 看第一个视频，不算我点的赞，看看评论区所有赞加起来有多少
    改进: 从APP数据源获取评论数据并计算点赞总数
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取评论数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili",
                   "cat", "files/video_comments.json"])

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
            comments_file_path = os.path.join(backup_dir, 'video_comments.json')
            with open(comments_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取评论数据，回退验证")
            return '9700' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 评论数据格式错误，回退验证")
            return '9700' in final_msg

        # 3. 计算评论区所有点赞数的总和（不包括当前用户点的赞）
        comments_list = data.get("comments", [])
        current_user_id = data.get("current_user_id", "user_current")

        total_likes = sum(
            comment.get("like_count", 0)
            for comment in comments_list
            if comment.get("user_id") != current_user_id
        )

        # 4. 验证 final_message 中是否包含正确答案
        if str(total_likes) in final_msg:
            print(f"✓ 验证成功: 评论区点赞总数（不含自己） = {total_likes}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={total_likes}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '9700' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '9700' in final_msg

if __name__ == '__main__':
    result = validate_task_17()
    print(result)

