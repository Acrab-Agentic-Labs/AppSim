# Task 28: 关注一个新的艺人
# Check: 通过 JSON 验证 followedArtists 数量是否比初始值增加
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_new_artist_followed(c: AppChecker):
    state = c.get_user_state()
    if not state:
        return result_fail("Check failed: unable to read user_state.json")

    followed = state.get("followedArtists", [])
    initial_followed = set(c.INITIAL_FOLLOWED_ARTISTS)
    newly_followed = [artist_id for artist_id in followed if artist_id not in initial_followed]

    if len(followed) > len(c.INITIAL_FOLLOWED_ARTISTS) and newly_followed:
        return result_pass("Check passed: a new artist was followed")

    return result_fail(
        "Check failed: no new followed artist found in user_state.json",
        {
            "initialFollowedArtists": c.INITIAL_FOLLOWED_ARTISTS,
            "followedArtists": followed,
            "newlyFollowedArtists": newly_followed,
        },
    )


if __name__ == "__main__":
    run_check(verify_new_artist_followed, 28)
