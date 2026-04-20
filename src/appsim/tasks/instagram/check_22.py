"""
检测脚本 #22: 打开一个聊天会话，发送消息'Hello, how are you?'
难度: 2 (中等)
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
                if "Hello, how are you?" in msg.get("text", ""):
                    return result_pass(f"消息已发送到会话 {conv['conversationId']} (JSON验证)")
        return result_fail("所有会话中都没有找到'Hello, how are you?'消息")

    # Fallback: UI check
    if ui.has_text("Hello, how are you?"):
        return result_pass("消息'Hello, how are you?'已成功发送")

    return result_fail("未检测到消息发送成功")


if __name__ == "__main__":
    run_check(check)
