# Task 29: 关注一个新的播客
# Check: 通过 JSON 验证 savedPodcasts 数量是否增加（初始为空）
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_new_podcast_followed(c: AppChecker):
    state = c.get_user_state()
    if not state:
        return result_fail("Check failed: unable to read user_state.json")

    podcasts = state.get("savedPodcasts", [])
    if len(podcasts) > 0:
        return result_pass("Check passed: a new podcast was followed")

    return result_fail(
        "Check failed: no saved podcast found in user_state.json",
        {"savedPodcasts": podcasts},
    )


if __name__ == "__main__":
    run_check(verify_new_podcast_followed, 29)
