"""
Check Script #3: Tell me how many contacts are on the current messages page
Difficulty: 1 (Easy)
Check Method: Check if on Messages page, count contacts/conversations
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if on Messages page
    if not ui.has_text("Messages"):
        return result_fail("Not on Messages page")

    # Count user items in conversation list
    all_texts = ui.get_all_texts()
    system_texts = {"Messages", "Requests", "Search", "", "messages", "New message"}
    contact_count = 0
    for text in all_texts:
        if text and text not in system_texts and not text.startswith("@"):
            contact_count += 1

    # Use content-desc to count user avatar count
    descs = ui.get_all_descs()
    avatar_count = sum(1 for d in descs if d and d not in ["Search", "New message", "Switch", "Messages", "Back", ""])

    # Take larger of two methods as contact count (text contains username+last message, so divide by 2)
    estimated = max(contact_count // 2, avatar_count)
    if estimated > 0:
        return result_pass(f"Messages page has approximately {estimated} contacts/conversations")

    if contact_count > 0:
        return result_pass(f"Messages page has approximately {contact_count} contact-related texts")

    return result_fail("Unable to count contacts")


if __name__ == "__main__":
    run_check(check)
