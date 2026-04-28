# Task 17: 关掉定时器
# Check: Sleep timer is turned off
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    # Read playback state from JSON
    playback_state = c.get_playback_state()

    if playback_state is None:
        return result_fail("Failed to read playback state")

    sleep_timer = playback_state.get("sleepTimerDuration")

    # Check if timer is turned off (None or null)
    if sleep_timer is None:
        return result_pass("Sleep timer is turned off", {"sleepTimerDuration": None})
    else:
        return result_fail(f"Sleep timer is still active", {"sleepTimerDuration": sleep_timer})


if __name__ == "__main__":
    run_check(check, 17)
