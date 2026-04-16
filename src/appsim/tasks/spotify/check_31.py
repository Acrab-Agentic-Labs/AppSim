# Task 31: 添加一首歌曲到Liked Songs
# Check: 通过 JSON 验证 likedSongs 数量是否比初始值增加
# Fallback: UI 上出现 "Unlike" 图标或 "Added" 提示
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        liked = state.get("likedSongs", [])
        # 初始有 2 首，添加后应 > 2
        if len(liked) > len(c.INITIAL_LIKED_SONGS):
            return True

    # Fallback: UI 验证
    return (
        c.find_text("Now Playing")
        or c.find_text_contains("Added")
        or c.find_desc("Unlike")
    )


if __name__ == "__main__":
    run_check(check, 31)
