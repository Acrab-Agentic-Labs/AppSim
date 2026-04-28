import logging

try:
    from ._device_utils import default_backup_dir, list_records, read_json_from_device
except ImportError:
    from _device_utils import default_backup_dir, list_records, read_json_from_device


DEFAULT_DEVICE_ID = "122.228.230.214:10343"
PACKAGE_NAME = "com.example.tencent_meeting_sim"
PERSONAL_MEETING_ID = "4157555988"
INVITATIONS_FILE = "meeting_invitations.json"
EXPECTED_ZHOU_USERS = {
    "user008": "\u5468\u5efa\u534e",
    "user033": "\u5468\u521a\u82b3",
    "user037": "\u5468\u6d9b",
    "user045": "\u5468\u9759\u56fd",
    "user053": "\u5468\u52c7\u52c7",
    "user084": "\u5468\u73cd",
    "user112": "\u5468\u519b",
    "user114": "\u5468\u9f99",
}


def _read_data(device_id, backup_dir, file_name):
    return list_records(
        read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{file_name}",
            backup_dir=backup_dir,
        )
    )


def _get_invitee_id(invitation):
    return invitation.get("inviteeId") or invitation.get("invitedUserId")


def _format_expected_users(user_ids):
    return [f"{user_id} {EXPECTED_ZHOU_USERS.get(user_id, '')}".strip() for user_id in sorted(user_ids)]


def check_personal_room_invitation(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """Verify operation-created invitations cover all Zhou-surname friends for user001's room."""

    del result
    effective_device_id = device_id or DEFAULT_DEVICE_ID
    if backup_dir is None:
        backup_dir = default_backup_dir("tencentmeeting_eval_29")

    invitations_data = _read_data(effective_device_id, backup_dir, INVITATIONS_FILE)
    expected_user_ids = set(EXPECTED_ZHOU_USERS)
    invited_zhou_users = {
        str(_get_invitee_id(invitation) or "")
        for invitation in invitations_data
        if str(invitation.get("meetingId")) == PERSONAL_MEETING_ID
    } & expected_user_ids

    missing_users = expected_user_ids - invited_zhou_users
    if missing_users:
        logging.error(
            "Missing Zhou-surname invitees for room %s: %s",
            PERSONAL_MEETING_ID,
            _format_expected_users(missing_users),
        )
        return False

    logging.info("All eight expected Zhou-surname users were invited to room %s.", PERSONAL_MEETING_ID)
    return True


if __name__ == "__main__":
    print(check_personal_room_invitation())
