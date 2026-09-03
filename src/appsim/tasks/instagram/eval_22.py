"""
Check Script #22: 打开与deepak.patel的聊天会话，发送消息'Hello, how are you?'
Difficulty: 2 (Medium)
Check Method: Read conversations_state.json to verify message sent to deepak.patel
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_chat_message_sent(adb, ui):
    # Read user state to get user mapping
    user_state = get_user_state(adb)

    # Primary: check via JSON state
    convs = get_conversations_state(adb)

    # Debug: print what we got
    if convs is None:
        return result_fail("Unable to read conversations_state.json from device")

    if not isinstance(convs, list):
        return result_fail(f"conversations_state.json has unexpected format: {type(convs)}")

    # Look for the message in deepak.patel's conversation
    # Accept both "Hello, how are you?" and "Hello,how are you?" (with or without spaces)
    target_messages = ["Hello, how are you?", "Hello,how are you?"]

    deepak_conv = None
    message_found_in_other_conv = False
    other_conv_info = None

    for conv in convs:
        participant_ids = conv.get("participantIds", [])

        # Check messages in this conversation
        for msg in conv.get("messages", []):
            msg_text = msg.get("text", "")
            # Check if message matches any of the target formats
            if any(target in msg_text for target in target_messages):
                if "user_deepak" in participant_ids:
                    # Found in correct conversation!
                    return result_pass(
                        f"Message 'Hello, how are you?' sent to deepak.patel",
                        {
                            "conversationId": conv.get("conversationId"),
                            "participantIds": participant_ids,
                            "messageText": msg_text,
                            "senderId": msg.get("senderId")
                        }
                    )
                else:
                    # Found but in wrong conversation
                    message_found_in_other_conv = True
                    other_conv_info = {
                        "conversationId": conv.get("conversationId"),
                        "participantIds": participant_ids,
                        "messageText": msg_text
                    }

    # Message found but not to deepak.patel
    if message_found_in_other_conv:
        return result_fail(
            "Message 'Hello, how are you?' sent but not to deepak.patel",
            other_conv_info
        )

    # Message not found at all
    return result_fail(
        "Message 'Hello, how are you?' not found in any conversation",
        {
            "totalConversations": len(convs),
            "conversationIds": [c.get("conversationId") for c in convs]
        }
    )


if __name__ == "__main__":
    run_check(verify_chat_message_sent)
