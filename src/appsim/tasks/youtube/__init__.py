from ..base import AppTasks, TaskItem

from .eval_1 import validate_task_one
from .eval_2 import validate_task_two
from .eval_3 import validate_task_three
from .eval_4 import validate_task_four
from .eval_5 import validate_task_five
from .eval_6 import validate_task_six
from .eval_7 import validate_task_seven
from .eval_8 import validate_task_eight
from .eval_9 import validate_task_nine
from .eval_10 import validate_task_ten
from .eval_11 import validate_task_eleven
from .eval_12 import validate_task_twelve
from .eval_13 import validate_task_thirteen
from .eval_14 import validate_task_fourteen
from .eval_15 import validate_task_fifteen
from .eval_16 import validate_task_sixteen
from .eval_17 import validate_task_seventeen
from .eval_18 import validate_task_eighteen
from .eval_19 import validate_task_nineteen
from .eval_20 import validate_task_twenty
from .eval_21 import validate_task_twenty_one
from .eval_22 import validate_task_twenty_two
from .eval_23 import validate_task_twenty_three
from .eval_24 import validate_task_twenty_four
from .eval_25 import validate_task_twenty_five
from .eval_26 import validate_task_twenty_six
from .eval_27 import validate_task_twenty_seven
from .eval_28 import validate_task_twenty_eight
from .eval_29 import validate_task_twenty_nine
from .eval_30 import validate_task_thirty
from .eval_31 import validate_task_thirty_one
from .eval_32 import validate_task_thirty_two
from .eval_33 import validate_task_thirty_three
from .eval_34 import validate_task_thirty_four
from .eval_35 import validate_task_thirty_five


YOUTUBE_TASKS = AppTasks(
    package_name="com.example.youtube_sim",
    task_items=[
        TaskItem(
            instruction='View my watch history',
            verify_func=validate_task_one,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Search for apple, then like and save the first video',
            verify_func=validate_task_two,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to watch an ITX PC build video. Search for itx and like the first video',
            verify_func=validate_task_three,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='View my liked videos, then play the song by the Chinese-language singer',
            verify_func=validate_task_four,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Turn on the subscriptions button',
            verify_func=validate_task_five,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Delete the last video in Watch later',
            verify_func=validate_task_six,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Subscribe to Jay Chou',
            verify_func=validate_task_seven,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Comment "This song is so beautiful" on Jay Chou 青花瓷',
            verify_func=validate_task_eight,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='On the History page, check how many Jay Chou MVs I have watched in total',
            verify_func=validate_task_nine,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check the duration of the first video in my liked videos',
            verify_func=validate_task_ten,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check whether restricted mode is on or off',
            verify_func=validate_task_eleven,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check whether the mentions button is on or off',
            verify_func=validate_task_twelve,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check the current App language option',
            verify_func=validate_task_thirteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='On the Apple section of the Home page, how many videos are about phones?',
            verify_func=validate_task_fourteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Search for iphone and check how many results this search has',
            verify_func=validate_task_fifteen,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how many related videos are shown below the first video's playback page on the Home page",
            verify_func=validate_task_sixteen,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='What is the total number of likes in the comments section of the first video on the Home page?',
            verify_func=validate_task_seventeen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check the total duration of the videos in Watch later',
            verify_func=validate_task_eighteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check the total duration of the videos in Liked videos',
            verify_func=validate_task_nineteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check Jay Chou's follower count",
            verify_func=validate_task_twenty,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Scroll through Shorts. Among the first four shorts you see, how many are about computers?',
            verify_func=validate_task_twenty_one,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Scroll through Shorts. Among the first four shorts you see, how many are about mini PCs?',
            verify_func=validate_task_twenty_two,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Scroll through Shorts. How many likes do the computer-related shorts among the first four shorts have in total?',
            verify_func=validate_task_twenty_three,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Scroll through Shorts. Among the first four shorts you see, what is the total duration in seconds of the computer-related shorts? Reply with the number of seconds only',
            verify_func=validate_task_twenty_four,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='In Jay Chou 夜曲 MV, how many likes does the newest comment have?',
            verify_func=validate_task_twenty_five,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='How many play records are in History?',
            verify_func=validate_task_twenty_six,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check the option selected for Video quality on mobile networks',
            verify_func=validate_task_twenty_seven,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Check the option selected for Video quality on Wi-Fi',
            verify_func=validate_task_twenty_eight,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Among the first six videos under All on the Home page, how many are about computers?',
            verify_func=validate_task_twenty_nine,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='What is the current app version number?',
            verify_func=validate_task_thirty,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Play Jay Chou 夜曲, choose Higher picture quality, and turn on Loop video and Stable volume',
            verify_func=validate_task_thirty_one,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Play Jay Chou 青花瓷, choose Higher picture quality, and turn off Ambient mode',
            verify_func=validate_task_thirty_two,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='First turn on Higher picture quality on the Quality page, then play Jay Chou 青花瓷 and comment "This MV looks really clear"',
            verify_func=validate_task_thirty_three,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Like, save, and comment "I have been a Jay Chou fan for ten years" on Jay Chou 夜曲, then like, save, and comment "This song reminds me of that girl" on 青花瓷',
            verify_func=validate_task_thirty_four,
            human_steps=24,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Like, save, and comment "Although your song sounds great, I still prefer listening to Jay Chou" on Taylor Swift\'s The Fate of Ophelia',
            verify_func=validate_task_thirty_five,
            human_steps=11,
            is_reasoning=False,
        ),
    ],
)
