"""
检测脚本 #32: 退出当前账号
难度: 3 (困难)
检测方式: 检查是否出现登录页面或退出确认
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 退出后可能出现登录页面
    if ui.has_text("Log in") and not ui.has_text("Log out"):
        return result_pass("已成功退出账号（显示登录页面）")

    # 可能出现退出确认对话框
    if ui.has_text("Log out") and ui.has_text("Are you sure"):
        return result_pass("退出确认对话框已出现")

    # 可能在Settings页面还没点Log out
    if ui.has_text("Settings") and ui.has_text("Log out"):
        return result_fail("在设置页面但尚未点击Log out")

    # 检查是否app已关闭/重启
    if not ui.xml or len(ui.xml) < 50:
        return result_pass("应用可能已退出")

    return result_fail("未检测到退出账号操作")


if __name__ == "__main__":
    run_check(check)
