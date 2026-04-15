from appsim.utils import read_json_from_device


PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
STATE_FILE_PATH = "files/task_state.json"
TARGETS = {
    "music-jay-chou-nocturne": "I have been a Jay Chou fan for ten years",
    "music-blue-porcelain": "This song reminds me of that girl",
}


def validate_task_thirty_four(result=None, device_id=None, backup_dir=None):
    try:
        message_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        state = read_json_from_device(device_id, PACKAGE_NAME, STATE_FILE_PATH, backup_dir)
        events = message_data if isinstance(message_data, list) else [message_data]
    except Exception:
        return False

    liked = {item_id: False for item_id in TARGETS}
    saved = {item_id: False for item_id in TARGETS}
    commented = {item_id: False for item_id in TARGETS}

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        item_id = extra_data.get("item_id")
        if item_id not in TARGETS:
            continue
        if event.get("action") == "toggle_video_like" and extra_data.get("enabled") == "true":
            liked[item_id] = True
        if event.get("action") == "toggle_video_save" and extra_data.get("enabled") == "true":
            saved[item_id] = True
        if event.get("action") == "submit_comment" and extra_data.get("text") == TARGETS[item_id]:
            commented[item_id] = True

    liked_video_ids = set(state.get("liked_video_ids", []))
    saved_video_ids = set(state.get("saved_video_ids", []))
    return all(
        liked[item_id]
        and saved[item_id]
        and commented[item_id]
        and item_id in liked_video_ids
        and item_id in saved_video_ids
        for item_id in TARGETS
    )


if __name__ == "__main__":
    print(validate_task_thirty_four())
