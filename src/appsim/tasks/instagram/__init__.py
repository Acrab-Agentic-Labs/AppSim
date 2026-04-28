from ..base import AppTasks, TaskItem
from .check_01 import check as check_01
from .check_02 import check as check_02
from .check_03 import check as check_03
from .check_04 import check as check_04
from .check_05 import check as check_05
from .check_06 import check as check_06
from .check_07 import check as check_07
from .check_08 import check as check_08
from .check_09 import check as check_09
from .check_10 import check as check_10
from .check_11 import check as check_11
from .check_12 import check as check_12
from .check_13 import check as check_13
from .check_14 import check as check_14
from .check_15 import check as check_15
from .check_16 import check as check_16
from .check_17 import check as check_17
from .check_18 import check as check_18
from .check_19 import check as check_19
from .check_20 import check as check_20
from .check_21 import check as check_21
from .check_22 import check as check_22
from .check_23 import check as check_23
from .check_24 import check as check_24
from .check_25 import check as check_25
from .check_26 import check as check_26
from .check_27 import check as check_27
from .check_28 import check as check_28
from .check_29 import check as check_29
from .check_30 import check as check_30
from .check_31 import check as check_31
from .check_32 import check as check_32
from .check_33 import check as check_33
from .check_34 import check as check_34
from .check_35 import check as check_35
from .check_36 import check as check_36
from .check_37 import check as check_37
from .check_38 import check as check_38
from .check_39 import check as check_39
from .check_40 import check as check_40

def validate_task(task_id):
    """Wrapper to convert check function to validate function signature"""
    def wrapper(result=None, device_id=None, backup_dir=None):
        from .common import get_adb, get_ui
        adb = get_adb(device_id)
        ui = get_ui(adb)
        check_func = globals()[f'check_{task_id:02d}']
        try:
            passed = check_func(adb, ui)
            return passed
        except Exception:
            return False
    return wrapper

INSTAGRAM_TASKS = AppTasks(
    package_name="com.example.myinstagram",
    task_items=[
        TaskItem(
            instruction="Tell me how many likes the first post on the homepage has",
            verify_func=validate_task(1),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Tell me how many likes the currently playing short video has",
            verify_func=validate_task(2),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Tell me how many contacts are on the current messages page",
            verify_func=validate_task(3),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Tell me the username of the current user",
            verify_func=validate_task(4),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Like the first post on the homepage",
            verify_func=validate_task(5),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Favorite the first post on the homepage",
            verify_func=validate_task(6),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Open the notifications page",
            verify_func=validate_task(7),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Go to the author profile of the first post on the homepage",
            verify_func=validate_task(8),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Repost the first post",
            verify_func=validate_task(9),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Swipe to view the next short video",
            verify_func=validate_task(10),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Edit gender on profile to female",
            verify_func=validate_task(11),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Search for content related to 'happy' on the search page",
            verify_func=validate_task(12),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Open the first conversation on the messages page",
            verify_func=validate_task(13),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Show me the first comment of the first post on the homepage",
            verify_func=validate_task(14),
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Share the first post on the homepage",
            verify_func=validate_task(15),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Share my personal QR code",
            verify_func=validate_task(16),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Mark the first post on the homepage as 'Not Interested'",
            verify_func=validate_task(17),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check my number of followers",
            verify_func=validate_task(18),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Like the currently playing short video",
            verify_func=validate_task(19),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check how many items are in my favorites collection",
            verify_func=validate_task(20),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Comment 'Nice!' under the second post on the homepage",
            verify_func=validate_task(21),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Open a chat with deepak.patel and send the message 'Hello, how are you?'",
            verify_func=validate_task(22),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Set my account to private",
            verify_func=validate_task(23),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Set daily usage time limit to 60 minutes",
            verify_func=validate_task(24),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Change my username to 'zhou'",
            verify_func=validate_task(25),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Follow the author of the third post on the homepage",
            verify_func=validate_task(26),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Randomly select a user and block them",
            verify_func=validate_task(27),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Randomly add a close friend",
            verify_func=validate_task(28),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Remove a follower named deepak.patel",
            verify_func=validate_task(29),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Enable Sleep Mode",
            verify_func=validate_task(30),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="View the first video on my profile",
            verify_func=validate_task(31),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Log out of the current account",
            verify_func=validate_task(32),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new collection named 'Favorites'",
            verify_func=validate_task(33),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new post: select the second picture from the album, set title 'Beautiful sunset', add hashtag #nature, add location 'Central Park', then post",
            verify_func=validate_task(34),
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new post: select any picture, enter a title, add a poll with question 'Which is better?' and options 'Option A' and 'Option B', then post",
            verify_func=validate_task(35),
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new post: select any picture, enter a title, add a music track by search, set audience to 'Close Friends', then post",
            verify_func=validate_task(36),
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Send 'I like your post!' to an unfollowed user",
            verify_func=validate_task(37),
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new post, hide like count, enable Facebook sharing",
            verify_func=validate_task(38),
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new post: select the second picture from the album, set title 'Beautiful sunset', add hashtag #nature, add location 'Central Park', hide like count, disable comments, then post",
            verify_func=validate_task(39),
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Post a short video",
            verify_func=validate_task(40),
            human_steps=5,
            is_reasoning=False,
        ),
    ],
)
