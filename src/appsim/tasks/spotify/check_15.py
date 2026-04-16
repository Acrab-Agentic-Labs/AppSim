# Task 15: 取消当前播放歌曲的收藏
# Check: 通过 JSON 验证 likedSongs 数量是否比初始值减少
# Fallback: UI 上出现 "Like"（而非 "Unlike"）
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        liked = state.get("likedSongs", [])
        # 初始有 2 首，取消收藏后应 < 2
        if len(liked) < len(c.INITIAL_LIKED_SONGS):
            return True

    # Fallback: UI 验证
    return (
        c.find_text("Now Playing")
        and c.find_desc("Like")
        and not c.find_desc("Unlike", timeout=1)
    )


if __name__ == "__main__":
    run_check(check, 15)
