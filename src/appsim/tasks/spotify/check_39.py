# Task 39: 已关注的歌手中，谁的作品数最多
# Check: 通过 JSON 验证已关注歌手的作品数，并检查答案是否正确
# Followed artists: Taylor Swift (artist_001, 3 songs), Ed Sheeran (artist_002, 3 songs)
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    state = c.get_user_state()
    if not state:
        return result_fail("Check failed: unable to read user_state.json")

    followed_artists = state.get("followedArtists", [])
    if not followed_artists:
        return result_fail("Check failed: no followed artists found")

    # 初始关注的艺人：artist_001 (Taylor Swift, 3首), artist_002 (Ed Sheeran, 3首)
    # 两者作品数相同，任一答案都正确
    expected_artists = ["artist_001", "artist_002"]
    expected_names = ["taylor swift", "ed sheeran", "taylor", "ed"]

    # 检查 AI 回答是否包含正确的歌手名称
    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        if any(name in final_msg for name in expected_names):
            return result_pass("Check passed: answer contains correct artist name")

    return result_fail(
        "Answer check failed: final_message does not contain Taylor Swift or Ed Sheeran",
        {"followedArtists": followed_artists, "expectedArtists": expected_artists},
    )


if __name__ == "__main__":
    run_check(check, 39)
