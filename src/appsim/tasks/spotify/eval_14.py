# Task 14: 将当前播放歌曲收藏
# Check: 通过 JSON 验证 likedSongs 数量是否比初始值增加
# Fallback: UI 上出现 "Unlike" 图标
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_current_song_liked(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        liked = state.get("likedSongs", [])
        # 初始有 2 首 liked songs，收藏后应该 > 2 或包含当前歌曲
        if len(liked) > len(c.INITIAL_LIKED_SONGS):
            return result_pass("Liked songs increased")
        # 检查 song_013 (IRIS OUT, 默认播放歌曲) 是否被收藏
        if "song_013" in liked:
            return result_pass("Song 013 is liked")

    # Fallback: UI 验证
    passed = c.find_desc("Unlike")
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(verify_current_song_liked, 14)
