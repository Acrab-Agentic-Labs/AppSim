# Task 16: 设置定时器时间为15min
# Check: Sleep timer has been set to 15 minutes
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    # Read playback state from JSON
    playback_state = c.get_playback_state()

    if playback_state is None:
        return result_fail("Failed to read playback state")

    sleep_timer = playback_state.get("sleepTimerDuration")

    # Check if timer is set to 15 minutes
    if sleep_timer == "15 minutes":
        return result_pass("Sleep timer set to 15 minutes", {"sleepTimerDuration": sleep_timer})
    else:
        return result_fail(f"Sleep timer not set to 15 minutes", {"sleepTimerDuration": sleep_timer})


if __name__ == "__main__":
    run_check(check, 16)
