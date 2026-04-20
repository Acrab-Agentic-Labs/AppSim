"""
检测脚本 #13: 查看消息页面的第一个会话
难度: 2 (中等)
检测方式: 检查是否进入了聊天详情页面
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # ChatDetailScreen 特征: 有Back按钮、Message...输入框
    has_back = "Back" in ui.get_all_descs()
    has_message_input = ui.has_text("Message...")

    if has_back and has_message_input:
        return result_pass("已成功打开第一个聊天会话")

    # 备选: 检查Send按钮
    if has_message_input:
        return result_pass("已进入聊天详情页面")

    # 检查是否还在消息列表
    if ui.has_text("Messages") and not has_message_input:
        return result_fail("仍在消息列表页面，未进入会话详情")

    return result_fail("未检测到聊天详情页面")


if __name__ == "__main__":
    run_check(check)
