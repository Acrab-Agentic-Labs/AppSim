from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
JAY_CHOU_IDS = {"music-jay-chou-i-do", "all-jay-chou-i-do"}


def validate_task_four(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    opened_liked_videos = False
    played_jay_chou = False

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        if event.get("action") == "open_page" and event.get("page") == "playlist:liked_videos":
            opened_liked_videos = True
        if event.get("action") == "play_video" and event.get("page") == "playlist:liked_videos" and extra_data.get("item_id") in JAY_CHOU_IDS:
            played_jay_chou = True

    return opened_liked_videos and played_jay_chou


if __name__ == "__main__":
    print(validate_task_four())
