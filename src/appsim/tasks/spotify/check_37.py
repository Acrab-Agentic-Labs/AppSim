# Task 37: 创建歌单 'My Punk', 搜索并添加 'Shape of You', 搜索并添加 'Style',
# 关注两条新的播客"The Daily"和"Crime Junkie"
# Check: 验证 "My Punk" 包含这两首具体的歌曲, savedPodcasts >= 2
from .check_common import AppChecker, run_check, result_pass, result_fail


# 'Shape of You' = song_004, 'Style' = song_003
EXPECTED_SONGS = {"song_004", "song_003"}


def check(c: AppChecker):
    # 验证 "My Punk" 歌单存在且包含指定歌曲
    playlists = c.get_user_playlists()
    if not playlists or not isinstance(playlists, list):
        return result_fail("Check failed: unable to read user_playlists.json")

    my_punk_playlist = None
    for p in playlists:
        if p.get("name") == "My Punk":
            my_punk_playlist = p
            break

    if not my_punk_playlist:
        return result_fail(
            "Check failed: 'My Punk' playlist not found",
            {"userPlaylists": playlists},
        )

    # 验证歌单包含 'Shape of You' (song_004) 和 'Style' (song_003)
    song_ids = set(my_punk_playlist.get("songIds", []))
    if not EXPECTED_SONGS.issubset(song_ids):
        missing_songs = EXPECTED_SONGS - song_ids
        return result_fail(
            f"Check failed: 'My Punk' playlist missing expected songs: {missing_songs}",
            {"playlist": my_punk_playlist, "expectedSongs": list(EXPECTED_SONGS), "actualSongs": list(song_ids)},
        )

    # 验证 savedPodcasts 增加至少2个
    user_state = c.get_user_state()
    if not user_state or not isinstance(user_state, dict):
        return result_fail("Check failed: unable to read user_state.json")

    saved_podcasts = user_state.get("savedPodcasts", [])
    if len(saved_podcasts) < 2:
        return result_fail(
            f"Check failed: saved podcasts count is {len(saved_podcasts)}, expected at least 2",
            {"savedPodcasts": saved_podcasts},
        )

    return result_pass(
        f"Check passed: 'My Punk' playlist with {len(song_ids)} songs, {len(saved_podcasts)} podcasts saved"
    )


if __name__ == "__main__":
    run_check(check, 37)
