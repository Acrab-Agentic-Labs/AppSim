try:
    from ._shared import _profile_state
except ImportError:
    from _shared import _profile_state  # type: ignore


PROFILE_UPDATE_TASK_ID = 16


def verify_personal_status_busy(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    profile = _profile_state(PROFILE_UPDATE_TASK_ID, device_id, backup_dir)
    return str(profile.get("availability", "")) == "Busy"


if __name__ == "__main__":
    print(verify_personal_status_busy())
