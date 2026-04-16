"""
检测脚本 #20: 查看个人收藏夹中有几个作品
难度: 2 (中等)
检测方式: 检查是否在Saved页面并能看到收藏的作品
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在Saved页面
    if not ui.has_text("Saved"):
        return result_fail("当前不在收藏夹页面")

    # 检查All Posts收藏夹
    if ui.has_text("All Posts"):
        return result_pass("已打开收藏夹页面，包含'All Posts'收藏夹")

    all_texts = ui.get_all_texts()
    # 查找收藏数量相关文本
    for text in all_texts:
        if re.match(r'^\d+\s*(items?|posts?|个)', text, re.IGNORECASE):
            return result_pass(f"收藏夹中有 {text}")

    # 在Saved页面但没有找到收藏内容
    descs = ui.get_all_descs()
    if "Back" in descs:
        return result_pass("已打开收藏夹页面（可能为空）")

    return result_fail("在Saved页面但无法确认收藏内容")


if __name__ == "__main__":
    run_check(check)
