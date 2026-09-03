from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
TARGET_TEXT = "This song is so beautiful"
TARGET_ITEM_ID = "music-blue-porcelain"


def verify_channel_video_commented(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        if event.get("action") != "submit_comment":
            continue
        if event.get("page") != "comments_sheet":
            continue
        if extra_data.get("item_id") == TARGET_ITEM_ID and extra_data.get("text") == TARGET_TEXT:
            return True
    return False


if __name__ == "__main__":
    print(verify_channel_video_commented())
