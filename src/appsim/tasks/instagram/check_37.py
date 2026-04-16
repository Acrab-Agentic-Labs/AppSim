"""
检测脚本 #37: 给未关注的陌生用户发送"I like your post!"
难度: 3 (困难)
检测方式: 读取 conversations_state.json 验证消息已发送
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    convs = get_conversations_state(adb)
    if convs:
        for conv in convs:
            for msg in conv.get("messages", []):
                if "I like your post!" in msg.get("text", ""):
                    return result_pass(f"消息已发送到会话 {conv['conversationId']} (JSON验证)")
        return result_fail("所有会话中都没有找到'I like your post!'消息")

    # Fallback: UI check
    if ui.has_text("I like your post!"):
        return result_pass("消息'I like your post!'已成功发送")

    if ui.has_text("Message..."):
        return result_fail("在聊天页面但未找到已发送的消息")

    return result_fail("未检测到消息发送成功")


if __name__ == "__main__":
    run_check(check)
