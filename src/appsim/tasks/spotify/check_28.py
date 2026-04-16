# Task 28: 关注一个新的艺人
# Check: 通过 JSON 验证 followedArtists 数量是否比初始值增加
# Fallback: UI 上出现 "Following" 按钮
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        followed = state.get("followedArtists", [])
        # 初始关注 2 个艺人，关注新的后应 > 2
        if len(followed) > len(c.INITIAL_FOLLOWED_ARTISTS):
            return True

    # Fallback: UI 验证
    return (
        c.find_text("Following")
        and (
            c.find_text("Add artists")
            or c.find_text("Artists you might like")
        )
    )


if __name__ == "__main__":
    run_check(check, 28)
