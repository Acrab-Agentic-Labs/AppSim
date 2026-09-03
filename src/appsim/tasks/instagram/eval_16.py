"""
Check Script #16: 分享个人二维码
Difficulty: 2 (Medium)
Check Method: Check if entered ShareProfile page and showing QR code
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_personal_qr_code_share_opened(adb, ui):
    # ShareProfileScreen features: QR Code, Share profile, Copy link
    descs = ui.get_all_descs()

    if ui.has_text("QR code") or "QR Code" in descs:
        return result_pass("Opened personal QR code share page")

    if ui.has_text("Share profile") and ui.has_text("Copy link"):
        return result_pass("Entered share profile page")

    # Check if on Profile page（还没点Share profile）
    if ui.has_text("Edit profile") and ui.has_text("Share profile"):
        return result_fail("Still on profile, not on QR code share page")

    return result_fail("QR code share page not detected")


if __name__ == "__main__":
    run_check(verify_personal_qr_code_share_opened)
