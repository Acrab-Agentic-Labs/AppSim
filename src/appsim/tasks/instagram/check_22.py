"""
Check Script #22: 打开一个聊天会话，发送消息'Hello, how are you?'
Difficulty: 2 (Medium)
Check Method: Read conversations_state.json to verify message sent
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Primary: check via JSON state
    convs = get_conversations_state(adb)
    if convs:
        for conv in convs:
            for msg in conv.get("messages", []):
                if "Hello, how are you?" in msg.get("text", ""):
                    return result_pass(f"Message sent to conversation {conv['conversationId']} (JSON验证)")
        return result_fail("'Hello, how are you?' message not found in any conversation")

    # Fallback: UI check
    if ui.has_text("Hello, how are you?"):
        return result_pass("Message 'Hello, how are you?' successfully sent")

    return result_fail("Message send success not detected")


if __name__ == "__main__":
    run_check(check)
