"""
检测脚本 #23: 将自己的账号设置为私密账户
难度: 2 (中等)
检测方式: 读取 user_state.json 验证 isPrivate 为 true
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        if user.get("isPrivate") is True:
            return result_pass("账号已设为私密 (JSON验证)")
        return result_fail(f"账号 isPrivate={user.get('isPrivate')}，未设为私密")

    # Fallback: UI check
    if ui.has_text("Account privacy") or ui.has_text("Private account"):
        nodes = ui.find_by_text_contains("Private account")
        if nodes:
            all_nodes_str = " ".join(nodes)
            if 'checked="true"' in all_nodes_str:
                return result_pass("私密账户已开启")

        xml = ui.xml
        switch_pattern = r'<node[^>]*class="[^"]*Switch[^"]*"[^>]*checked="true"[^>]*/>'
        if re.search(switch_pattern, xml):
            return result_pass("私密账户开关已开启")

        return result_fail("Private account开关可能未开启")

    return result_fail("当前不在Account Privacy页面")


if __name__ == "__main__":
    run_check(check)
