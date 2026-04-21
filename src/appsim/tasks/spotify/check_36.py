# Task 36: 取消关注Taylor Swift
# Check: 通过 JSON 验证 followedArtists 中不再包含 artist_001 (Taylor Swift)
# Fallback: UI 验证 - Taylor Swift 页面显示 Follow 而非 Following，或音乐库中无 Taylor Swift
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        followed = state.get("followedArtists", [])
        # artist_001 是 Taylor Swift 的 ID
        if "artist_001" not in followed:
            return result_pass("Taylor Swift unfollowed")

    # Fallback: UI 验证
    # Case 1: On Taylor Swift's artist page, Follow button visible (unfollowed state)
    if c.find_text("Taylor Swift") and c.find_desc("Back"):
        if c.find_text("Follow") and not c.find_text("Following"):
            return result_pass("Follow button visible")

    passed = False
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 36)
