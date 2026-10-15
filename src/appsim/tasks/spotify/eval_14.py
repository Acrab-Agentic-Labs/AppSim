# Task 14: 将当前播放歌曲收藏
# Check: 通过 JSON 验证 likedSongs 数量是否比初始值增加
from .check_common import AppChecker, result_fail, result_pass, run_check


def verify_current_song_liked(c: AppChecker):
    state = c.get_user_state()
    if state is None:
        # No UI fallback: the seeded home screen already shows an "Unlike" icon
        return result_fail("Failed to read user state")

    liked = state.get("likedSongs", [])
    # 初始有 2 首 liked songs，收藏后应该 > 2 或包含当前歌曲
    if len(liked) > len(c.INITIAL_LIKED_SONGS):
        return result_pass("Liked songs increased")
    # 检查 song_013 (IRIS OUT, 默认播放歌曲) 是否被收藏
    if "song_013" in liked:
        return result_pass("Song 013 is liked")
    return result_fail("Current song not liked")


if __name__ == "__main__":
    run_check(verify_current_song_liked, 14)
