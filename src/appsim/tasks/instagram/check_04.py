"""
检测脚本 #4: 告诉我当前用户的用户名
难度: 1 (简单)
检测方式: 进入Profile页面，提取用户名信息
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在Profile页面
    if ui.has_text("Edit profile") or ui.has_text("Share profile"):
        # 在Profile页面，用户名通常显示在顶部
        all_texts = ui.get_all_texts()
        # 用户名通常是第一个非空文本或带有@前缀的文本
        for text in all_texts:
            if text and text not in ["Edit profile", "Share profile", "Posts", "Followers", "Following", "Profile", ""]:
                return result_pass(f"当前用户名: {text}")

    # 也可能在其他页面，检查顶部标题栏
    descs = ui.get_all_descs()
    for desc in descs:
        if desc == "Profile":
            return result_fail("在Profile标签但未能提取用户名，请确保已打开Profile页面")

    return result_fail("当前不在个人主页，无法获取用户名")


if __name__ == "__main__":
    run_check(check)
