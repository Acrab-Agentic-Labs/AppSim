"""
检测脚本 #3: 告诉我当前消息页面有几个联系人
难度: 1 (简单)
检测方式: 检查是否在Messages页面，统计联系人/会话数量
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在Messages页面
    if not ui.has_text("Messages"):
        return result_fail("当前不在消息页面")

    # 统计会话列表中的用户项
    all_texts = ui.get_all_texts()
    system_texts = {"Messages", "Requests", "Search", "", "messages", "New message"}
    contact_count = 0
    for text in all_texts:
        if text and text not in system_texts and not text.startswith("@"):
            contact_count += 1

    # 使用content-desc来统计用户头像数量
    descs = ui.get_all_descs()
    avatar_count = sum(1 for d in descs if d and d not in ["Search", "New message", "Switch", "Messages", "Back", ""])

    # 取两种方式中较大的作为联系人数（文本包含用户名+最后消息，所以除以2）
    estimated = max(contact_count // 2, avatar_count)
    if estimated > 0:
        return result_pass(f"消息页面约有 {estimated} 个联系人/会话")

    if contact_count > 0:
        return result_pass(f"消息页面约有 {contact_count} 个联系人相关文本")

    return result_fail("无法统计联系人数量")


if __name__ == "__main__":
    run_check(check)
