"""
检测脚本 #8: 查看首页中第一个帖子的作者主页
难度: 1 (简单)
检测方式: 检查是否进入了其他用户的Profile页面
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # OtherUserProfileScreen 包含 Follow/Following 按钮和 Message 按钮
    descs = ui.get_all_descs()

    # 检查是否在其他用户Profile页面
    has_back = "Back" in descs
    has_follow = ui.has_text("Follow") or ui.has_text("Following")
    has_message = ui.has_text("Message")
    has_posts = ui.has_text("Posts")

    if has_back and has_follow and has_message:
        return result_pass("已成功进入帖子作者的个人主页")

    if has_back and has_posts and (has_follow or ui.has_text("Followers")):
        return result_pass("已进入用户主页")

    # 检查是否有用户名和帖子网格
    if has_back and ui.has_text("Followers") and ui.has_text("Following"):
        return result_pass("已进入用户主页（含粉丝/关注数据）")

    return result_fail("未检测到用户主页页面")


if __name__ == "__main__":
    run_check(check)
