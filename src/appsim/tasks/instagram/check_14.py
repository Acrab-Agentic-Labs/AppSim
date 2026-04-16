"""
检测脚本 #14: 查看首页第一个帖子的第一条评论并告诉我
难度: 2 (中等)
检测方式: 检查评论弹窗是否打开并显示评论内容
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查Comments底部弹窗是否打开
    if ui.has_text("Comments") and ui.has_text("Add a comment"):
        # 尝试获取评论文本
        all_texts = ui.get_all_texts()
        # 排除系统文本
        system_texts = {"Comments", "Add a comment...", "Post", "Add a comment", ""}
        comments = [t for t in all_texts if t not in system_texts and len(t) > 2]
        if comments:
            return result_pass(f"评论弹窗已打开，第一条评论相关文本: {comments[0]}")
        return result_pass("评论弹窗已打开（但可能没有评论）")

    if ui.has_text("Comments"):
        return result_pass("评论弹窗已打开")

    return result_fail("评论弹窗未打开")


if __name__ == "__main__":
    run_check(check)
