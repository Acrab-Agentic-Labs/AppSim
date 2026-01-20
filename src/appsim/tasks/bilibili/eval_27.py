import subprocess
import json
import os
import re

def validate_task_27(result=None, device_id=None, backup_dir=None):
    """
    任务27: 在首页第一条视频评论页面，找到一条点赞数最高的评论，看看up主的名字叫什么
    改进: 从APP数据源获取评论数据并查找点赞数最高的评论的up主
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
            return '用户1号' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 评论数据格式错误，回退验证")
            return '用户1号' in final_msg

        # 3. 查找点赞数最高的评论的用户名字
        comments_list = data.get("comments", [])
        if not comments_list:
            print("⚠️ 评论列表为空，回退验证")
            return '用户1号' in final_msg

        # 找到点赞数最高的评论
        max_like_comment = max(comments_list, key=lambda x: x.get("like_count", 0))
        uploader_name = max_like_comment.get("user_name", "")

        # 4. 验证 final_message 中是否包含正确答案
        if uploader_name and uploader_name in final_msg:
            print(f"✓ 验证成功: 点赞数最高的评论的up主 = {uploader_name}")
            return True
        else:
            print(f"❌ 验证失败: 期望up主={uploader_name}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '用户1号' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '用户1号' in final_msg

if __name__ == '__main__':
    result = validate_task_27()
    print(result)
