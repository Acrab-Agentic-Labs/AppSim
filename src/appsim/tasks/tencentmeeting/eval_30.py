import logging


def check_personal_room_invitation(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """
    验证个人会议室是否邀请了所有周姓好友

    Args:
        user_id: 用户ID
        expected_invited_count: 期望邀请的周姓用户数量
        device_id: 设备ID
        backup_dir: 备份目录

    Returns:
        bool: 验证是否通过
    """

    # 使用常量
    user_id = USER_ID
    expected_invited_count = EXPECTED_INVITED_COUNT

    from ..utils import pull_and_parse_json

    try:
        # 读取用户数据，找出所有周姓用户
        users_data = pull_and_parse_json(
            device_id=device_id or "emulator-5554",
            remote_path="files/users.json",
            backup_dir=backup_dir,
        )

        zhou_users = [u for u in users_data if u.get("username", "").startswith("周")]
        zhou_user_ids = {u.get("userId") for u in zhou_users}

        logging.info(f"找到 {len(zhou_users)} 个周姓用户: {zhou_user_ids}")

        # 读取个人会议室配置，获取meetingId
        rooms_data = pull_and_parse_json(
            device_id=device_id or "emulator-5554",
            remote_path="files/personal_meeting_rooms.json",
            backup_dir=backup_dir,
        )

        user_room = next((r for r in rooms_data if r.get("userId") == user_id), None)
        if not user_room:
            logging.error(f"未找到用户 {user_id} 的个人会议室")
            return False

        personal_meeting_id = user_room.get("meetingId")

        # 读取邀请记录
        invitations_data = pull_and_parse_json(
            device_id=device_id or "emulator-5554",
            remote_path="files/meeting_invitations.json",
            backup_dir=backup_dir,
        )

        # 检查哪些周姓用户被邀请了
        invited_zhou_users = set()
        for invitation in invitations_data:
            if invitation.get("meetingId") == personal_meeting_id:
                invited_user_id = invitation.get("inviteeId")  # 注意字段名
                if invited_user_id in zhou_user_ids:
                    invited_zhou_users.add(invited_user_id)

        logging.info(f"已邀请的周姓用户: {invited_zhou_users}")

        # 验证是否所有周姓用户都被邀请了
        if len(invited_zhou_users) >= expected_invited_count:
            logging.info(f"✅ 邀请验证成功：已邀请 {len(invited_zhou_users)} 个周姓用户")
            return True
        else:
            missing_users = zhou_user_ids - invited_zhou_users
            logging.error(f"验证失败：部分周姓用户未被邀请。缺失的用户ID: {missing_users}")
            return False

    except Exception as e:
        logging.error(f"验证过程出错: {str(e)}")
        return False


if __name__ == '__main__':
    print(check_personal_room_invitation())
