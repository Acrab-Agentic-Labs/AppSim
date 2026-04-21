import logging


DEFAULT_DEVICE_ID = "122.228.230.214:10343"
USER_ID = "user001"
EXPECTED_INVITED_COUNT = 5


def check_personal_room_invitation(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """Verify the personal room invited all users whose usernames start with 周."""

    user_id = USER_ID
    expected_invited_count = EXPECTED_INVITED_COUNT

    from ..utils import pull_and_parse_json

    effective_device_id = device_id or DEFAULT_DEVICE_ID

    try:
        users_data = pull_and_parse_json(
            device_id=effective_device_id,
            remote_path="files/users.json",
            backup_dir=backup_dir,
        )

        zhou_users = [u for u in users_data if u.get("username", "").startswith("周")]
        zhou_user_ids = {u.get("userId") for u in zhou_users}

        logging.info(f"找到 {len(zhou_users)} 个周姓用户: {zhou_user_ids}")

        rooms_data = pull_and_parse_json(
            device_id=effective_device_id,
            remote_path="files/personal_meeting_rooms.json",
            backup_dir=backup_dir,
        )

        user_room = next((r for r in rooms_data if r.get("userId") == user_id), None)
        if not user_room:
            logging.error(f"未找到用户 {user_id} 的个人会议室")
            return False

        personal_meeting_id = user_room.get("meetingId")

        invitations_data = pull_and_parse_json(
            device_id=effective_device_id,
            remote_path="files/meeting_invitations.json",
            backup_dir=backup_dir,
        )

        invited_zhou_users = set()
        for invitation in invitations_data:
            if invitation.get("meetingId") == personal_meeting_id:
                invited_user_id = invitation.get("inviteeId")
                if invited_user_id in zhou_user_ids:
                    invited_zhou_users.add(invited_user_id)

        logging.info(f"已邀请的周姓用户: {invited_zhou_users}")

        if len(invited_zhou_users) >= expected_invited_count:
            logging.info(f"邀请验证成功: 已邀请 {len(invited_zhou_users)} 个周姓用户")
            return True

        missing_users = zhou_user_ids - invited_zhou_users
        logging.error(f"验证失败，仍有周姓用户未被邀请: {missing_users}")
        return False

    except Exception as e:
        logging.error(f"验证过程出错: {str(e)}")
        return False


if __name__ == "__main__":
    print(check_personal_room_invitation())
