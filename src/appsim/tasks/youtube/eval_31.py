from appsim.utils import read_json_from_device


PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
STATE_FILE_PATH = "files/task_state.json"
TARGET_ITEM_ID = "music-jay-chou-nocturne"
TARGET_PAGE = f"video_play:{TARGET_ITEM_ID}"


def validate_task_thirty_one(result=None, device_id=None, backup_dir=None):
    try:
        message_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        state = read_json_from_device(device_id, PACKAGE_NAME, STATE_FILE_PATH, backup_dir)
        events = message_data if isinstance(message_data, list) else [message_data]
    except Exception:
        return False

    played_target = False
    selected_quality = False
    enabled_loop = False
    enabled_stable_volume = False

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        if event.get("action") == "play_video" and extra_data.get("item_id") == TARGET_ITEM_ID:
            played_target = True
        if event.get("action") == "select_option" and event.get("page") == TARGET_PAGE:
            if (
                extra_data.get("group_key") == "quality_current_video"
                and extra_data.get("option_key") == "higher_picture_quality"
                and extra_data.get("item_id") == TARGET_ITEM_ID
            ):
                selected_quality = True
        if event.get("action") == "toggle_setting" and event.get("page") == TARGET_PAGE:
            if extra_data.get("item_id") != TARGET_ITEM_ID:
                continue
            if extra_data.get("key") == "loop_video" and extra_data.get("enabled") == "true":
                enabled_loop = True
            if extra_data.get("key") == "stable_volume" and extra_data.get("enabled") == "true":
                enabled_stable_volume = True

    toggle_states = state.get("toggle_states", {})
    selected_options = state.get("selected_options", {})
    return (
        played_target
        and selected_quality
        and enabled_loop
        and enabled_stable_volume
        and selected_options.get("quality_current_video") == "higher_picture_quality"
        and toggle_states.get("loop_video") is True
        and toggle_states.get("stable_volume") is True
    )


if __name__ == "__main__":
    print(validate_task_thirty_one())
