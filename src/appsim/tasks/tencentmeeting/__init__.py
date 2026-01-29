# 所有指令 - 文件编号与任务序号一致
from ..base import AppTasks, TaskItem

# ============================================================================
# 任务1-34的导入 (eval_1.py to eval_34.py)
# ============================================================================
from .eval_1 import check_recent_ended_meeting
from .eval_2 import check_previous_meeting_playback
from .eval_3 import check_join_meeting_with_password
from .eval_4 import check_screen_sharing
from .eval_5 import check_hand_raise
from .eval_6 import check_search_user_by_phone
from .eval_7 import verify_invitation_link_copied
from .eval_8 import verify_meeting_count
from .eval_9 import verify_contact_count
from .eval_10 import verify_participant_count_in_meeting
from .eval_11 import verify_not_started_meeting_count
from .eval_12 import verify_surname_zhou_count
from .eval_13 import verify_phone_13_count
from .eval_14 import verify_invitable_people_count
from .eval_15 import check_mic_enabled
from .eval_16 import check_camera_enabled
from .eval_17 import check_all_mics_muted
from .eval_18 import check_message_content
from .eval_19 import check_quick_meeting_created
from .eval_20 import check_scheduled_meeting_with_all_friends
from .eval_21 import get_latest_ended_meeting_details
from .eval_22 import check_screen_sharing_active
from .eval_23 import check_personal_meeting_room_waiting_room_status
from .eval_24 import verify_upcoming_meetings_with_password
from .eval_25 import verify_chensiyuan_max_participants_meeting
from .eval_26 import verify_message_count_by_sender
from .eval_27 import verify_average_meeting_duration
from .eval_28 import verify_most_active_sender
from .eval_29 import check_personal_meeting_room_settings
from .eval_30 import check_personal_room_invitation
from .eval_31 import check_participant_management
from .eval_32 import check_selective_meeting_invitation
from .eval_33 import check_personal_room_advanced_settings
from .eval_34 import check_message_and_handraise

TENCENT_MEETING_TASKS = AppTasks(
    package_name="com.example.tencent_meeting_sim",
    task_items=[
        # 1
        TaskItem(
            instruction="查看历史会议记录",
            verify_func=check_recent_ended_meeting,
            human_steps=1,
            is_reasoning=False,
            skip=True,
        ),
        # 2
        TaskItem(
            instruction="在历史会议里观看最近一次会议的回放",
            verify_func=check_previous_meeting_playback,
            human_steps=3,
            is_reasoning=False,
            skip=True,
        ),
        # 3
        TaskItem(
            instruction="用会议号 341234546 + 密码 312435 加入会议",
            verify_func=check_join_meeting_with_password,
            human_steps=6,
            is_reasoning=False,
            skip=True,
        ),
        # 4
        TaskItem(
            instruction="在技术方案讨论会议中，开启 '共享屏幕'",
            verify_func=check_screen_sharing,
            human_steps=2,
            is_reasoning=False,
            skip=True,
        ),
        # 5
        TaskItem(
            instruction="在技术讨论会议中举手发言",
            verify_func=check_hand_raise,
            human_steps=2,
            is_reasoning=False,
            skip=True,
        ),
        # 6
        TaskItem(
            instruction="在联系人列表中查看手机号为15823467912的联系人信息",
            verify_func=check_search_user_by_phone,
            human_steps=4,
            is_reasoning=True,
            skip=True,
        ),
        # 7
        TaskItem(
            instruction="复制我的个人会议室链接",
            verify_func=verify_invitation_link_copied,
            human_steps=3,
            is_reasoning=False,
            skip=True,
        ),
        # 8
        TaskItem(
            instruction="数一下会议列表中的会议数目",
            verify_func=verify_meeting_count,
            human_steps=1,
            is_reasoning=True,
            skip=True,
        ),
        # 9
        TaskItem(
            instruction="数一下我的联系人数目",
            verify_func=verify_contact_count,
            human_steps=3,
            is_reasoning=True,
            skip=True,
        ),
        # 10
        TaskItem(
            instruction="数一下我的会议室的参会人数",
            verify_func=verify_participant_count_in_meeting,
            human_steps=5,
            is_reasoning=True,
            skip=True,
        ),
        # 11
        TaskItem(
            instruction="数一下未开始会议的数目",
            verify_func=verify_not_started_meeting_count,
            human_steps=1,
            is_reasoning=True,
            skip=True,
        ),
        # 12
        TaskItem(
            instruction="数一下周姓的人数",
            verify_func=verify_surname_zhou_count,
            human_steps=3,
            is_reasoning=True,
            skip=True,
        ),
        # 13
        TaskItem(
            instruction="数一下手机号13开头的人数",
            verify_func=verify_phone_13_count,
            human_steps=3,
            is_reasoning=True,
            skip=True,
        ),
        # 14
        TaskItem(
            instruction="数一下技术讨论会议（meeting_3d7e91）中可邀请的人员数量",
            verify_func=verify_invitable_people_count,
            human_steps=5,
            is_reasoning=True,
            skip=True,
        ),
        # 15
        TaskItem(
            instruction="在技术讨论会议（会议号Meeting_3d7e91）中打开自己的麦克风",
            verify_func=check_mic_enabled,
            human_steps=2,
            is_reasoning=False,
            skip=True,
        ),
        # 16
        TaskItem(
            instruction="在技术讨论会议（会议号Meeting_3d7e91）中打开自己的摄像头",
            verify_func=check_camera_enabled,
            human_steps=2,
            is_reasoning=False,
            skip=True,
        ),
        # 17
        TaskItem(
            instruction="在技术讨论会议（会议号Meeting_3d7e91）中关闭所有人的麦克风",
            verify_func=check_all_mics_muted,
            human_steps=3,
            is_reasoning=False,
            skip=True,
        ),
        # 18
        TaskItem(
            instruction='在技术讨论会议（会议号Meeting_3d7e91）中发送消息"大家好"',
            verify_func=check_message_content,
            human_steps=3,
            is_reasoning=False,
            skip=True,
        ),
        # 19
        TaskItem(
            instruction="保持默认配置创建一场快速会议",
            verify_func=check_quick_meeting_created,
            human_steps=3,
            is_reasoning=False,
            skip=True,
        ),
        # 20
        TaskItem(
            instruction="预约一场会议，时间定为明天晚上八点",
            verify_func=check_scheduled_meeting_with_all_friends,
            human_steps=5,
            is_reasoning=False,
        ),
        # 21
        TaskItem(
            instruction="查看最近一场会议的会议主题和会议时长",
            verify_func=get_latest_ended_meeting_details,
            human_steps=3,
            is_reasoning=True,
            skip=True,
        ),
        # 22
        TaskItem(
            instruction="加入会议号为Meeting_5d8e21的会议，然后共享屏幕",
            verify_func=check_screen_sharing_active,
            human_steps=3,
            is_reasoning=False,
            skip=True,
        ),
        # 23
        TaskItem(
            instruction='将"个人会议室"的"等候室"设置为"开启"，然后进入会议室',
            verify_func=check_personal_meeting_room_waiting_room_status,
            human_steps=4,
            is_reasoning=False,
            skip=True,
        ),
        # 24
        TaskItem(
            instruction="数一下未开始会议的数目",
            verify_func=verify_upcoming_meetings_with_password,
            human_steps=3,
            is_reasoning=True,
            skip=True,
        ),
        # 25
        TaskItem(
            instruction="帮我查看一下，陈思远创建的所有会议中，参与人数最多的会议主题是什么？",
            verify_func=verify_chensiyuan_max_participants_meeting,
            human_steps=5,
            is_reasoning=True,
            skip=True,
        ),
        # 26
        TaskItem(
            instruction="帮我统计一下，技术讨论会议中，陈思远发送了多少条消息？",
            verify_func=verify_message_count_by_sender,
            human_steps=5,
            is_reasoning=True,
            skip=True,
        ),
        # 27
        TaskItem(
            instruction="帮我计算一下，所有已结束会议的平均时长是多少分钟？",
            verify_func=verify_average_meeting_duration,
            human_steps=3,
            is_reasoning=True,
            skip=True,
        ),
        # 28
        TaskItem(
            instruction="帮我看看，技术讨论会议中，谁发送的消息最多？",
            verify_func=verify_most_active_sender,
            human_steps=5,
            is_reasoning=True,
            skip=True,
        ),
        # 29
        TaskItem(
            instruction='设置我的个人会议室，设置会议密码为"648723"，启用等候室，将成员入会时静音设置为"始终关闭"',
            verify_func=check_personal_meeting_room_settings,
            human_steps=5,
            is_reasoning=False,
            skip=True,
        ),
        # 30
        TaskItem(
            instruction='进入个人会议室，邀请所有周姓好友参加',
            verify_func=check_personal_room_invitation,
            human_steps=20,
            is_reasoning=False,
            skip=True,
        ),
        # 31
        TaskItem(
            instruction="进入会议号为meeting_3d7e91的会议，将所有参与者静音",
            verify_func=check_participant_management,
            human_steps=6,
            is_reasoning=False,
            skip=True,
        ),
        # 32
        TaskItem(
            instruction='创建一场会议，主题为"新产品发布"',
            verify_func=check_selective_meeting_invitation,
            human_steps=5,
            is_reasoning=True,
            skip=True,
        ),
        # 33
        TaskItem(
            instruction='进入个人会议室设置，修改会议密码为"888888"',
            verify_func=check_personal_room_advanced_settings,
            human_steps=5,
            is_reasoning=False,
            skip=True,
        ),
        # 34
        TaskItem(
            instruction='进入技术讨论会议，发送消息"我有问题"，然后举手发言',
            verify_func=check_message_and_handraise,
            human_steps=5,
            is_reasoning=False,
            skip=True,
        ),
    ],
)
