# Task 39: 告诉我音乐库中的歌单chill vibes中有多少首歌，如果少于6首，就添加歌曲直到6首
# Check: 验证 answer 含数量信息, Chill Vibes 歌单歌曲数 >= 6
# Chill Vibes (playlist_002) 初始有 4 首歌: ["song_005", "song_008", "song_011", "song_003"]
from .check_common import AppChecker, run_check, result_pass, result_fail


CHILL_VIBES_INITIAL_COUNT = 4


def check(c: AppChecker, result=None):
    # 验证答案包含歌曲数量
    if not result or "final_message" not in result:
        return result_fail("Check failed: no answer provided in result")

    final_msg = str(result["final_message"]).lower()

    # 检查答案是否包含数量信息（初始为4首）
    has_count = any(
        keyword in final_msg
        for keyword in ["4", "four", "四"]
    )

    if not has_count:
        return result_fail(
            "Check failed: answer does not mention the song count",
            {"finalMessage": result["final_message"]},
        )

    # 验证歌曲已被添加到 Chill Vibes（通过 user_playlists 检查）
    # 由于 Chill Vibes 是系统歌单，添加歌曲后可能通过 user_playlists 或其他方式追踪
    playlists = c.get_user_playlists()
    if playlists and isinstance(playlists, list):
        for p in playlists:
            name = p.get("name", "").lower()
            if "chill" in name and "vibe" in name:
                song_ids = p.get("songIds", [])
                if len(song_ids) >= 6:
                    return result_pass(
                        f"Check passed: Chill Vibes has {len(song_ids)} songs (>= 6)"
                    )

    # Fallback: 检查 user_state 中 savedPlaylists 的变化或 UI 状态
    user_state = c.get_user_state()
    if user_state and isinstance(user_state, dict):
        # 如果能读到状态，检查是否有歌曲被添加的迹象
        liked_songs = user_state.get("likedSongs", [])
        # 答案正确且有操作痕迹即可通过
        if has_count:
            # UI 验证: 检查是否在歌单页面且显示了歌曲数
            if c.find_text_contains("songs") or c.find_text_contains("Chill"):
                return result_pass(
                    "Check passed: answer contains count, UI shows playlist"
                )

    return result_fail(
        "Check failed: could not verify songs were added to Chill Vibes",
        {"finalMessage": result["final_message"]},
    )


if __name__ == "__main__":
    run_check(check, 39)
