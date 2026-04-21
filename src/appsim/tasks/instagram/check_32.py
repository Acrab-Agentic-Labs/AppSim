"""
Check Script #32: 退出当前账号
Difficulty: 3 (Hard)
Check Method: Check if login page or logout confirmation appeared
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # After logout may show login page
    if ui.has_text("Log in") and not ui.has_text("Log out"):
        return result_pass("Successfully logged out (login page shown)")

    # May show logout confirmation dialog
    if ui.has_text("Log out") and ui.has_text("Are you sure"):
        return result_pass("Logout confirmation dialog appeared")

    # May be on Settings page, Log out not clicked yet
    if ui.has_text("Settings") and ui.has_text("Log out"):
        return result_fail("On Settings page but Log out not clicked")

    # Check if app closed/restarted
    if not ui.xml or len(ui.xml) < 50:
        return result_pass("App may have exited")

    return result_fail("Logout action not detected")


if __name__ == "__main__":
    run_check(check)
