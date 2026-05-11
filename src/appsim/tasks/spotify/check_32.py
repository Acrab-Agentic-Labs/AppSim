# Task 32: 搜索歌曲Blank Space，并收藏，告诉我第一句歌词, 查看制作人员并告诉我作词人是谁
# Check: 验证 likedSongs 增加, answer 含歌词和作词人信息
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 验证 likedSongs 增加
    user_state = c.get_user_state()
    if not user_state or not isinstance(user_state, dict):
        return result_fail("Check failed: unable to read user_state.json")

    liked_songs = user_state.get("likedSongs", [])
    if len(liked_songs) <= len(c.INITIAL_LIKED_SONGS):
        return result_fail(
            "Check failed: liked songs did not increase",
            {"likedSongs": liked_songs, "initialLikedSongs": c.INITIAL_LIKED_SONGS},
        )

    # 验证答案包含歌词和作词人信息
    if not result or "final_message" not in result:
        return result_fail("Check failed: no answer provided in result")

    final_msg = str(result["final_message"]).lower()

    # 检查是否包含歌词信息
    has_lyrics = any(
        keyword in final_msg
        for keyword in ["i close my eyes", "close my eyes", "lyric", "歌词", "first line"]
    )

    # 检查是否包含作词人信息
    has_lyricist = any(
        keyword in final_msg
        for keyword in ["taylor swift", "kenshi yonezu", "lyricist", "作词", "songwriter", "written by"]
    )

    if not has_lyrics or not has_lyricist:
        return result_fail(
            "Check failed: answer does not contain required lyrics and lyricist information",
            {"finalMessage": result["final_message"]},
        )

    return result_pass(
        "Check passed: liked songs increased, answer contains lyrics and lyricist info"
    )


if __name__ == "__main__":
    run_check(check, 32)
