"""
Check Script #37: 给未关注的陌生用户发送"I like your post!"
Difficulty: 3 (Hard)
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
                if "I like your post!" in msg.get("text", ""):
                    return result_pass(f"Message sent to conversation {conv['conversationId']} (JSON验证)")
        return result_fail("'I like your post!' message not found in any conversation")

    # Fallback: UI check
    if ui.has_text("I like your post!"):
        return result_pass("Message 'I like your post!' successfully sent")

    if ui.has_text("Message..."):
        return result_fail("On chat page but sent message not found")

    return result_fail("Message send success not detected")


if __name__ == "__main__":
    run_check(check)
