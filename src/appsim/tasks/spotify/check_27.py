# Task 27: 创建歌单 'Workout', 添加歌曲'In your eyes'并关注这首歌的歌手
# Check: 验证 "Workout" 歌单包含 'In Your Eyes', followedArtists 增加
from .check_common import AppChecker, run_check, result_pass, result_fail


# 'In Your Eyes' = song_009 (The Weeknd / artist_003)
EXPECTED_SONG = "song_009"
EXPECTED_ARTIST = "artist_003"


def check(c: AppChecker):
    # 验证 "Workout" 歌单存在且包含 'In Your Eyes'
    playlists = c.get_user_playlists()
    if not playlists or not isinstance(playlists, list):
        return result_fail("Check failed: unable to read user_playlists.json")

    workout_playlist = None
    for p in playlists:
        if p.get("name") == "Workout":
            workout_playlist = p
            break

    if not workout_playlist:
        return result_fail(
            "Check failed: 'Workout' playlist not found",
            {"userPlaylists": playlists},
        )

    song_ids = workout_playlist.get("songIds", [])
    if EXPECTED_SONG not in song_ids:
        return result_fail(
            f"Check failed: 'Workout' playlist does not contain 'In Your Eyes' ({EXPECTED_SONG})",
            {"playlist": workout_playlist, "expectedSong": EXPECTED_SONG},
        )

    # 验证 followedArtists 增加（应该关注了 The Weeknd / artist_003）
    user_state = c.get_user_state()
    if not user_state or not isinstance(user_state, dict):
        return result_fail("Check failed: unable to read user_state.json")

    followed_artists = user_state.get("followedArtists", [])
    if len(followed_artists) <= len(c.INITIAL_FOLLOWED_ARTISTS):
        return result_fail(
            "Check failed: followed artists did not increase",
            {"followedArtists": followed_artists, "initialFollowedArtists": c.INITIAL_FOLLOWED_ARTISTS},
        )

    return result_pass(
        f"Check passed: 'Workout' playlist with {len(song_ids)} song(s), followed artists increased"
    )


if __name__ == "__main__":
    run_check(check, 27)
