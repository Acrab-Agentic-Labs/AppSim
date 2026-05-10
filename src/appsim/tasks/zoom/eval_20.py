try:
    from ._shared import _profile_state
except ImportError:
    from _shared import _profile_state  # type: ignore


PROFILE_UPDATE_TASK_ID = 16


def verify_change_display_name_to_liu_chenlong(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    profile = _profile_state(PROFILE_UPDATE_TASK_ID, device_id, backup_dir)
    return str(profile.get("displayName", "")) == "Liu Chenlong"


if __name__ == "__main__":
    print(verify_change_display_name_to_liu_chenlong())
