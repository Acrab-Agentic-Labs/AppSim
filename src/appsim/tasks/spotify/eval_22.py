# Task 22: 搜索歌曲'Perfect', 并收藏
# Check: 验证 likedSongs 包含 song_005 (Perfect) 或数量增加
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_searched_song_liked(c: AppChecker):
    user_state = c.get_user_state()
    if not user_state or not isinstance(user_state, dict):
        return result_fail("Check failed: unable to read user_state.json")

    liked_songs = user_state.get("likedSongs", [])

    # Perfect 的 ID 是 song_005
    if "song_005" in liked_songs:
        return result_pass("Check passed: 'Perfect' (song_005) is in likedSongs")

    # Fallback: 检查 likedSongs 数量是否增加
    if len(liked_songs) > len(c.INITIAL_LIKED_SONGS):
        return result_pass("Check passed: likedSongs count increased")

    return result_fail(
        "Check failed: 'Perfect' not found in likedSongs and count did not increase",
        {"likedSongs": liked_songs, "initialLikedSongs": c.INITIAL_LIKED_SONGS},
    )


if __name__ == "__main__":
    run_check(verify_searched_song_liked, 22)
