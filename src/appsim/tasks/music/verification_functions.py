"""
音乐App自动化测试验证函数
用于验证各项任务是否成功完成
"""

import json
import os
import subprocess

# App包名
APP_PACKAGE = "com.example.netease_cloud_music_sim"


def read_json_from_device(file_path, device_id=None, result=None, backup_dir=None):
    """
    从设备读取JSON文件
    :param file_path: 设备上的文件路径(相对于app私有目录)
    :param backup_dir: 本地备份目录,用于存储从设备拉取的文件
    :return: JSON数据或None
    """
    try:
        # 优先使用 backup_dir 构造路径
        if backup_dir:
            local_file = os.path.join(backup_dir, os.path.basename(file_path))
        else:
            # 如果没有提供 backup_dir, 使用临时文件
            local_file = f"temp_{os.path.basename(file_path)}"

        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])

        cmd.extend(["exec-out", "run-as", APP_PACKAGE, "cat", f"files/{file_path}"])

        # 确保目录存在
        if backup_dir:
            os.makedirs(backup_dir, exist_ok=True)

        with open(local_file, "w", encoding="utf-8") as f_out:
            subprocess.run(cmd, stdout=f_out, stderr=subprocess.DEVNULL)

        # 读取JSON
        with open(local_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 如果使用的是临时文件, 则删除
        if not backup_dir:
            os.remove(local_file)
        return data
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}")
        return None