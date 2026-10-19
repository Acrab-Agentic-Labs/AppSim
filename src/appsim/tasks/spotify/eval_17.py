# Task 17: 关掉定时器
# Check: playback_state.json 中不再有活动的 sleepTimerDuration
#
# 前置条件：App 启动时自带一个已开启的睡眠定时器（MainActivity 里 seed 为 "30 minutes"）。
# SleepTimerView 只有在定时器激活时才渲染 "Turn off timer"，所以没有这个 seed 时
# "什么都没做"和"把定时器关掉"的设备状态完全一致（Gson 序列化会省略 null 的 sleepTimerDuration），
# 检查就会退化成"零交互即通过"。seed 之后，未关闭时该键为 "30 minutes"，关闭后才消失。
from .check_common import AppChecker, result_fail, result_pass, run_check

# 关闭状态下的可能取值，正常情况该键会被 Gson 直接省略
_OFF_VALUES = {"", "off", "none"}


def _active_sleep_timer(playback_state):
    """有活动定时器时返回其取值，定时器已关闭时返回 None。"""
    value = playback_state.get("sleepTimerDuration")
    if isinstance(value, str):
        return None if value.strip().lower() in _OFF_VALUES else value
    return value


def verify_sleep_timer_disabled(c: AppChecker):
    playback_state = c.get_playback_state()

    if playback_state is None:
        return result_fail("Failed to read playback state")

    sleep_timer = _active_sleep_timer(playback_state)
    details = {"sleepTimerDuration": playback_state.get("sleepTimerDuration")}

    if sleep_timer is None:
        return result_pass("Sleep timer is turned off", details)
    return result_fail(f"Sleep timer is still active: {sleep_timer}", details)


if __name__ == "__main__":
    run_check(verify_sleep_timer_disabled, 17)
