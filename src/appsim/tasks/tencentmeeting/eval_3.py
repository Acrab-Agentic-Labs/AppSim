import logging
import os

try:
    from ._device_utils import default_backup_dir, list_records, read_json_from_device
except ImportError:
    from _device_utils import default_backup_dir, list_records, read_json_from_device


PACKAGE_NAME = "com.example.tencent_meeting_sim"
MEETING_ID = "341234546"
PASSWORD = "312435"
USER_ID = "user001"
MEETINGS_FILE = "meetings.json"
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
BASELINE_MATCH_COUNT = 1
BASELINE_MAX_JOIN_TIME = 1697760272454


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def check_join_meeting_with_password(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """Pass only when joining created a participant record newer than baseline."""

    del result
    if backup_dir is None:
        backup_dir = default_backup_dir("tencentmeeting_eval_3")

    meetings = list_records(
        read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{MEETINGS_FILE}",
            backup_dir=backup_dir,
        )
    )
    meeting = next((item for item in meetings if str(item.get("meetingId")) == MEETING_ID), None)
    if meeting is None:
        logging.error("Meeting %s was not found in %s.", MEETING_ID, MEETINGS_FILE)
        return False
    if str(meeting.get("password")) != PASSWORD:
        logging.error("Meeting %s does not have the expected password.", MEETING_ID)
        return False

    participants = list_records(
        read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{MEETING_PARTICIPANTS_FILE}",
            backup_dir=backup_dir,
        )
    )
    matches = [
        participant
        for participant in participants
        if str(participant.get("userId")) == USER_ID and str(participant.get("meetingId")) == MEETING_ID
    ]
    if not matches:
        logging.error("No participant record exists for %s in meeting %s.", USER_ID, MEETING_ID)
        return False

    join_times = [_to_int(participant.get("joinTime")) for participant in matches]
    has_new_count = len(matches) > BASELINE_MATCH_COUNT
    has_new_join_time = any(join_time is not None and join_time > BASELINE_MAX_JOIN_TIME for join_time in join_times)

    if not (has_new_count or has_new_join_time):
        logging.error(
            "Participant state is still at baseline: count=%s, joinTimes=%s.",
            len(matches),
            join_times,
        )
        return False
    return True


if __name__ == "__main__":
    print(check_join_meeting_with_password())
