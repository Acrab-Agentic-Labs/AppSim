"""
检测脚本 #16: 分享个人二维码
难度: 2 (中等)
检测方式: 检查是否进入ShareProfile页面并显示QR码
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # ShareProfileScreen 特征: QR Code, Share profile, Copy link
    descs = ui.get_all_descs()

    if ui.has_text("QR code") or "QR Code" in descs:
        return result_pass("已打开个人二维码分享页面")

    if ui.has_text("Share profile") and ui.has_text("Copy link"):
        return result_pass("已进入分享个人资料页面")

    # 检查是否在Profile页面（还没点Share profile）
    if ui.has_text("Edit profile") and ui.has_text("Share profile"):
        return result_fail("仍在个人主页，未进入分享二维码页面")

    return result_fail("未检测到二维码分享页面")


if __name__ == "__main__":
    run_check(check)
