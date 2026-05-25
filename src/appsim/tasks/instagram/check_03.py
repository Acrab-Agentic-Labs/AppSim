"""
Check Script #3: Tell me how many contacts are on the current messages page
Difficulty: 1 (Easy)
Check Method: Check if on Messages page, count contacts/conversations, verify answer
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui, result=None):
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

    # Take larger of two methods as contact count
    estimated = max(contact_count // 2, avatar_count)

    if estimated <= 0 and contact_count <= 0:
        return result_fail("Unable to count contacts")

    count_str = str(estimated) if estimated > 0 else str(contact_count)

    if result and isinstance(result, dict):
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict):
            count_val = extracted_answer.get("count")
            if count_val is not None and int(count_val) == int(count_str):
                return result_pass(f"Messages page has {count_str} contacts, answer correct")

    return result_fail(f"Answer does not contain correct contact count ({count_str})")


if __name__ == "__main__":
    run_check(check)
