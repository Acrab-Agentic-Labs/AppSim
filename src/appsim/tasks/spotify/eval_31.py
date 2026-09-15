# Task 31: 添加一首歌曲到Liked Songs
# Check: 通过 JSON 验证 likedSongs 数量是否比初始值增加
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_song_added_to_liked_songs(c: AppChecker):
    state = c.get_user_state()
    if not state:
        return result_fail("Check failed: unable to read user_state.json")

    liked = state.get("likedSongs", [])
    initial_liked = set(c.INITIAL_LIKED_SONGS)
    newly_liked = [song_id for song_id in liked if song_id not in initial_liked]

    if len(liked) > len(c.INITIAL_LIKED_SONGS) and newly_liked:
        return result_pass("Check passed: a new song was added to Liked Songs")

    return result_fail(
        "Check failed: no new liked song found in user_state.json",
        {
            "initialLikedSongs": c.INITIAL_LIKED_SONGS,
            "likedSongs": liked,
            "newlyLikedSongs": newly_liked,
        },
    )


if __name__ == "__main__":
    run_check(verify_song_added_to_liked_songs, 31)
