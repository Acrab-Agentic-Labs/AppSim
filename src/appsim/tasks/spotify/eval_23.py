# Task 23: 创建歌单 'My Jazz', 搜索并添加歌曲'Shape of You' 和 'Style'
# Check: 验证歌单存在且包含这两首具体的歌曲
from .check_common import AppChecker, run_check, result_pass, result_fail


# 'Shape of You' = song_004, 'Style' = song_003
EXPECTED_SONGS = {"song_004", "song_003"}


def verify_playlist_created_with_songs(c: AppChecker):
    # 验证 JSON 中存在 "My Jazz" 歌单
    playlists = c.get_user_playlists()
    if not playlists or not isinstance(playlists, list):
        return result_fail("Check failed: unable to read user_playlists.json")

    # 查找 "My Jazz" 歌单
    my_jazz = None
    for p in playlists:
        if p.get("name") == "My Jazz":
            my_jazz = p
            break

    if not my_jazz:
        return result_fail(
            "Check failed: 'My Jazz' playlist not found",
            {"userPlaylists": playlists},
        )

    # 验证歌单包含 'Shape of You' (song_004) 和 'Style' (song_003)
    song_ids = set(my_jazz.get("songIds", []))

    if not EXPECTED_SONGS.issubset(song_ids):
        missing_songs = EXPECTED_SONGS - song_ids
        return result_fail(
            f"Check failed: 'My Jazz' playlist missing expected songs: {missing_songs}",
            {"playlist": my_jazz, "expectedSongs": list(EXPECTED_SONGS), "actualSongs": list(song_ids)},
        )

    return result_pass(
        f"Check passed: 'My Jazz' playlist created with 'Shape of You' and 'Style' (total {len(song_ids)} songs)"
    )


if __name__ == "__main__":
    run_check(verify_playlist_created_with_songs, 23)
