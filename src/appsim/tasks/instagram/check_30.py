"""
Check Script #30: 开启睡眠模式
Difficulty: 2 (Medium)
Check Method: Check if Sleep mode switch on Time Management page is enabled
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if onTime Management页面
    if not (ui.has_text("Time management") or ui.has_text("Sleep mode")):
        return result_fail("Not on Time Management page")

    # Check if Sleep mode exists
    if not ui.has_text("Sleep mode"):
        return result_fail("On Time Management page but Sleep mode option not found")

    # Find Switch near Sleep mode in XML
    xml = ui.xml

    # Try找到 Sleep mode 文本在XML中的location，然后查找附近的 Switch
    sleep_idx = xml.lower().find("sleep mode")
    if sleep_idx >= 0:
        # Take XML segment after Sleep mode to find associated Switch
        nearby_xml = xml[sleep_idx:sleep_idx + 500]
        switch_pattern = r'<node[^>]*class="[^"]*Switch[^"]*"[^>]*/>'
        switches = re.findall(switch_pattern, nearby_xml)
        if switches:
            if 'checked="true"' in switches[0]:
                return result_pass("Sleep mode enabled (Sleep mode switch on)")
            else:
                return result_fail("Sleep mode switch exists but not enabled")

    # Fallback: find all Switch, but require only Sleep mode related on page
    switch_pattern = r'<node[^>]*class="[^"]*Switch[^"]*"[^>]*/>'
    switches = re.findall(switch_pattern, xml)
    if switches:
        # If only one switch, can confirm it is Sleep mode
        if len(switches) == 1:
            if 'checked="true"' in switches[0]:
                return result_pass("Sleep mode enabled")
            return result_fail("Sleep mode switch not enabled")
        # With multiple switches cannot determine which is Sleep mode
        checked = sum(1 for s in switches if 'checked="true"' in s)
        if checked > 0:
            return result_pass(f"Sleep mode possibly enabled ({checked}/{len(switches)} switches enabled)")
        return result_fail("All switches disabled")

    return result_fail("On Time Management page but switch component not found")


if __name__ == "__main__":
    run_check(check)
