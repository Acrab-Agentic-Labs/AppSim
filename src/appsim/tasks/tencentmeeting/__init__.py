# 所有指令
from ..base import TaskItem, AppTasks

from .eval_3 import check_recent_ended_meeting
from .eval_8 import check_previous_meeting_playback
from .eval_9 import check_join_meeting_with_password
from .eval_11 import check_screen_sharing
from .eval_12 import check_hand_raise
from .eval_17 import check_search_user_by_phone, verify_search_result
from .eval_20 import check_contact_and_invitation_link, check_contacts_list, verify_invitation_link_copied
from .eval_21 import eval_21
from .eval_22 import eval_22
from .eval_23 import eval_23
from .eval_24 import eval_24
from .eval_25 import eval_25
from .eval_26 import eval_26
from .eval_27 import eval_27

TENCENT_MEETING_TASKS = AppTasks(
    package_name="com.example.tencentmeeting",
    task_items=[
        TaskItem(instruction="查看历史会议记录", verify_func=check_recent_ended_meeting),
        TaskItem(instruction="在历史会议里观看最近一次会议的回放", verify_func=check_previous_meeting_playback),
        TaskItem(instruction="用会议号 341234546 + 密码 312435 加入会议", verify_func=check_join_meeting_with_password),
        TaskItem(instruction="在技术方案讨论中，开启 '共享屏幕'", verify_func=check_screen_sharing),
        TaskItem(instruction="在技术方案讨论中举手发言", verify_func=check_hand_raise),
        TaskItem(instruction="呼叫手机号为15823467912的联系人", verify_func=check_search_user_by_phone),
        TaskItem(instruction="复制我的邀请链接让别人加我为好友", verify_func=check_contact_and_invitation_link),
        TaskItem(instruction="数一下会议列表中的会议数目", verify_func=eval_21),
        TaskItem(instruction="数一下我的联系人数目", verify_func=eval_22),
        TaskItem(instruction="数一下我的会议室的参会人数", verify_func=eval_23),
        TaskItem(instruction="数一下未开始会议的数目", verify_func=eval_24),
        TaskItem(instruction="数一下周姓的人数", verify_func=eval_25),
        TaskItem(instruction="计算手机号13开头的人数", verify_func=eval_26),
        TaskItem(instruction="数一下会议中可邀请的人员数量", verify_func=eval_27),
    ],
)

# 为了向后兼容，保留 ALL_INSTRUCTION
ALL_INSTRUCTION = [{"instruct": item.instruction, "fun": item.verify_func} for item in TENCENT_MEETING_TASKS.task_items]
