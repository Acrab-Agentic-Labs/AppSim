# 所有指令
# type: ignore
# noqa
from ..base import AppTasks, NumericReasoningCategory, TaskItem

# ============================================================================
# 任务导入
# ============================================================================

from .eval_1 import verify_meeting_history_opened
from .eval_2 import verify_recent_meeting_replay_opened
from .eval_3 import verify_meeting_joined_with_password
from .eval_4 import verify_screen_sharing_enabled
from .eval_5 import TASK5_ANSWER_SCHEMA, verify_meeting_count
from .eval_6 import TASK6_ANSWER_SCHEMA, verify_contact_count
from .eval_7 import TASK7_ANSWER_SCHEMA, verify_upcoming_meeting_count
from .eval_8 import TASK8_ANSWER_SCHEMA, verify_contacts_by_surname_count
from .eval_9 import TASK9_ANSWER_SCHEMA, verify_contacts_by_phone_prefix_count
from .eval_10 import TASK10_ANSWER_SCHEMA, verify_invitable_participant_count
from .eval_11 import verify_all_meeting_mics_muted
from .eval_12 import verify_latest_meeting_message_sent
from .eval_13 import verify_quick_meeting_created
from .eval_14 import verify_scheduled_meeting_created
from .eval_15 import TASK15_ANSWER_SCHEMA, verify_latest_ended_meeting_details
from .eval_16 import verify_screen_sharing_active
from .eval_17 import TASK17_ANSWER_SCHEMA, verify_sender_message_count
from .eval_18 import TASK18_ANSWER_SCHEMA, verify_average_ended_meeting_duration
from .eval_19 import TASK19_ANSWER_SCHEMA, verify_most_active_meeting_sender
from .eval_20 import verify_personal_meeting_room_settings
from .eval_21 import verify_personal_room_invitees_added
from .eval_22 import verify_meeting_participant_mute_state
from .eval_23 import verify_selected_meeting_invitees_added
from .eval_24 import verify_meeting_message_and_hand_raise
from .eval_25 import verify_hand_raise_and_contact_lookup
from .eval_26 import TASK26_ANSWER_SCHEMA, verify_personal_room_link_copied_and_participant_count

TENCENT_MEETING_TASKS = AppTasks(
    package_name="com.example.tencent_meeting_sim",
    task_items=[
        # 1
        TaskItem(
            instruction="查看历史会议记录",
            verify_func=verify_meeting_history_opened,
            human_steps=1,
        ),
        # 2
        TaskItem(
            instruction="在历史会议里观看最近一次会议的回放",
            verify_func=verify_recent_meeting_replay_opened,
            human_steps=3,
        ),
        # 3
        TaskItem(
            instruction="用会议号 341234546 + 密码 312435 加入会议",
            verify_func=verify_meeting_joined_with_password,
            human_steps=4,
        ),
        # 4
        TaskItem(
            instruction="在技术方案讨论会议中，开启 '共享屏幕'",
            verify_func=verify_screen_sharing_enabled,
            human_steps=2,
        ),
        # 5
        TaskItem(
            instruction="数一下会议列表中的会议数目",
            verify_func=verify_meeting_count,
            human_steps=1,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        # 6
        TaskItem(
            instruction="数一下我的联系人数目",
            verify_func=verify_contact_count,
            human_steps=15,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK6_ANSWER_SCHEMA,
        ),
        # 7
        TaskItem(
            instruction="数一下未开始会议的数目",
            verify_func=verify_upcoming_meeting_count,
            human_steps=1,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK7_ANSWER_SCHEMA,
        ),
        # 8
        TaskItem(
            instruction="数一下周姓的人数",
            verify_func=verify_contacts_by_surname_count,
            human_steps=15,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK8_ANSWER_SCHEMA,
        ),
        # 9
        TaskItem(
            instruction="数一下手机号13开头的人数",
            verify_func=verify_contacts_by_phone_prefix_count,
            human_steps=15,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK9_ANSWER_SCHEMA,
        ),
        # 10
        TaskItem(
            instruction="数一下技术讨论会议（meeting_3d7e91）中可邀请的人员数量",
            verify_func=verify_invitable_participant_count,
            human_steps=15,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK10_ANSWER_SCHEMA,
        ),
        # 11
        TaskItem(
            instruction="在技术讨论会议（会议号Meeting_3d7e91）中关闭所有人的麦克风",
            verify_func=verify_all_meeting_mics_muted,
            human_steps=3,
        ),
        # 12
        TaskItem(
            instruction="在技术讨论会议（会议号Meeting_3d7e91）中发送消息\"大家好\"",
            verify_func=verify_latest_meeting_message_sent,
            human_steps=5,
        ),
        # 13
        TaskItem(
            instruction="保持默认配置创建一场快速会议",
            verify_func=verify_quick_meeting_created,
            human_steps=2,
        ),
        # 14
        TaskItem(
            instruction="预约一场会议，时间定为明天晚上八点",
            verify_func=verify_scheduled_meeting_created,
            human_steps=10,
        ),
        # 15
        TaskItem(
            instruction="查看最近一场会议的会议主题和会议时长",
            verify_func=verify_latest_ended_meeting_details,
            human_steps=2,
            evaluation_type="answer",
            answer_schema=TASK15_ANSWER_SCHEMA,
        ),
        # 16
        TaskItem(
            instruction="加入会议号为Meeting_5d8e21的会议，然后共享屏幕",
            verify_func=verify_screen_sharing_active,
            human_steps=4,
        ),
        # 17
        TaskItem(
            instruction="帮我统计一下，技术讨论会议中，陈思远发送了多少条消息？",
            verify_func=verify_sender_message_count,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK17_ANSWER_SCHEMA,
        ),
        # 18
        TaskItem(
            instruction="帮我计算一下，所有已结束会议的平均时长是多少分钟？",
            verify_func=verify_average_ended_meeting_duration,
            human_steps=39,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        # 19
        TaskItem(
            instruction="帮我看看，技术讨论会议中，谁发送的消息最多？",
            verify_func=verify_most_active_meeting_sender,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK19_ANSWER_SCHEMA,
        ),
        # 20
        TaskItem(
            instruction="设置我的个人会议室，设置会议密码为\"648723\"，启用等候室，将成员入会时静音设置为\"始终关闭\"",
            verify_func=verify_personal_meeting_room_settings,
            human_steps=9,
        ),
        # 21
        TaskItem(
            instruction="进入个人会议室，邀请所有周姓好友参加",
            verify_func=verify_personal_room_invitees_added,
            human_steps=20,
        ),
        # 22
        TaskItem(
            instruction="进入会议号为meeting_3d7e91的会议，将所有参与者静音",
            verify_func=verify_meeting_participant_mute_state,
            human_steps=5,
        ),
        # 23
        TaskItem(
            instruction="创建一场会议，主题为\"新产品发布\"",
            verify_func=verify_selected_meeting_invitees_added,
            human_steps=3,
        ),
        # 24
        TaskItem(
            instruction="进入技术讨论会议，发送消息\"我有问题\"，然后举手发言",
            verify_func=verify_meeting_message_and_hand_raise,
            human_steps=6,
        ),
        # 25
        TaskItem(
            instruction="在技术讨论会议中举手发言，并在联系人列表中查看手机号为15823467912的联系人信息",
            verify_func=verify_hand_raise_and_contact_lookup,
            human_steps=6,
        ),
        # 26
        TaskItem(
            instruction="复制我的个人会议室链接，并数一下我的会议室的参会人数",
            verify_func=verify_personal_room_link_copied_and_participant_count,
            human_steps=8,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="hybrid",
            answer_schema=TASK26_ANSWER_SCHEMA,
        ),
    ],
)
