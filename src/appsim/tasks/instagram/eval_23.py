"""
Check Script #23: 将自己的账号设置为私密账户
Difficulty: 2 (Medium)
Check Method: Read user_state.json to verify isPrivate is true
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_private_account_enabled(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        if user.get("isPrivate") is True:
            return result_pass("Account set to private (JSON verified)")
        return result_fail(f"Account isPrivate={user.get('isPrivate')}, not set to private")

    # Fallback: UI check
    if ui.has_text("Account privacy") or ui.has_text("Private account"):
        nodes = ui.find_by_text_contains("Private account")
        if nodes:
            all_nodes_str = " ".join(nodes)
            if 'checked="true"' in all_nodes_str:
                return result_pass("Private account enabled")

        xml = ui.xml
        switch_pattern = r'<node[^>]*class="[^"]*Switch[^"]*"[^>]*checked="true"[^>]*/>'
        if re.search(switch_pattern, xml):
            return result_pass("Private account switch enabled")

        return result_fail("Private account switch may not be enabled")

    return result_fail("Not on Account Privacy page")


if __name__ == "__main__":
    run_check(verify_private_account_enabled)
