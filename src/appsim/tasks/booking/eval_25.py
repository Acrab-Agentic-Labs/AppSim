try:
    from ._shared import (
        ACTION_PROFILE_UPDATED,
        _current_user,
        _latest_account_action,
        _result_contains_any_group,
    )
except ImportError:
    from _shared import (  # type: ignore
        ACTION_PROFILE_UPDATED,
        _current_user,
        _latest_account_action,
        _result_contains_any_group,
    )


PROFILE_UPDATE_TASK_ID = 22


def verify_update_profile_first_name_to_peter(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    user = _current_user(PROFILE_UPDATE_TASK_ID, device_id, backup_dir)
    profile_action = _latest_account_action(
        PROFILE_UPDATE_TASK_ID,
        device_id,
        backup_dir,
        action_type=ACTION_PROFILE_UPDATED,
        field_name="name",
    )
    json_ok = bool(user and str(user.get("firstName", "")) == "Peter" and profile_action)
    fallback_ok = _result_contains_any_group(result, [["peter"]], broad=True)
    return json_ok or fallback_ok


if __name__ == "__main__":
    print(verify_update_profile_first_name_to_peter())
