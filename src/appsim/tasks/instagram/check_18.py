"""
检测脚本 #18: 查看个人粉丝数量
难度: 2 (中等)
检测方式: 检查是否在Followers/Following页面或Profile页面能看到粉丝数
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在Profile页面（含Followers/Following信息）
    if ui.has_text("Followers") and ui.has_text("Following"):
        all_texts = ui.get_all_texts()

        # 查找 "123 Followers" 或紧跟 Followers 的数字
        for text in all_texts:
            if "Followers" in text and any(c.isdigit() for c in text):
                return result_pass(f"找到粉丝数量: {text}")

        # 查找独立数字（可能是粉丝数）
        for text in all_texts:
            if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
                return result_pass(f"找到数字（粉丝数）: {text}")

        # 在Profile页面有Followers标签但没有找到具体数字
        return result_fail("在页面上看到Followers标签但未找到具体数字")

    # 检查是否在Profile页面
    if ui.has_text("Edit profile"):
        if ui.has_text("Followers"):
            # Profile页面有Followers标签
            all_texts = ui.get_all_texts()
            for text in all_texts:
                if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
                    return result_pass(f"在个人主页找到粉丝数量: {text}")
            return result_fail("在个人主页但未找到具体粉丝数字")

    return result_fail("未找到粉丝数量信息")


if __name__ == "__main__":
    run_check(check)
