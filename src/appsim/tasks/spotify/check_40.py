# Task 40: 目前音乐库中有多少首喜欢的歌曲
# Check: 通过 JSON 验证 likedSongs 的数量等于 2（初始值）
# Fallback: UI 上出现 Liked Songs 页面
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        liked = state.get("likedSongs", [])
        # 默认初始有 2 首喜欢的歌曲
        if len(liked) == 2:
            return True

    # Fallback: UI 验证
    return (
        c.find_text("Liked Songs")
        and c.find_desc("Back")
        and (
            c.find_text_contains("songs")
            or c.find_desc("Shuffle")
        )
    )


if __name__ == "__main__":
    run_check(check, 40)
