from ..base import AppTasks, TaskItem
from .check_1 import check as check_1
from .check_2 import check as check_2
from .check_3 import check as check_3
from .check_4 import check as check_4
from .check_5 import check as check_5
from .check_6 import check as check_6
from .check_7 import check as check_7
from .check_8 import check as check_8
from .check_9 import check as check_9
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
from .eval_2 import TASK2_ANSWER_SCHEMA, validate as validate_eval_2
from .eval_3 import TASK3_ANSWER_SCHEMA, validate as validate_eval_3
from .eval_4 import TASK4_ANSWER_SCHEMA, validate as validate_eval_4
from .eval_5 import TASK5_ANSWER_SCHEMA, validate as validate_eval_5
from .eval_6 import TASK6_ANSWER_SCHEMA, validate as validate_eval_6
from .eval_7 import TASK7_ANSWER_SCHEMA, validate as validate_eval_7
from .eval_8 import TASK8_ANSWER_SCHEMA, validate as validate_eval_8
from .eval_9 import TASK9_ANSWER_SCHEMA, validate as validate_eval_9
from .eval_18 import TASK18_ANSWER_SCHEMA, validate as validate_eval_18
from .eval_19 import TASK19_ANSWER_SCHEMA, validate as validate_eval_19
from .eval_20 import TASK20_ANSWER_SCHEMA, validate as validate_eval_20
from .eval_32 import TASK32_ANSWER_SCHEMA, validate as validate_eval_32
from .eval_34 import TASK34_ANSWER_SCHEMA, validate as validate_eval_34
from .eval_38 import TASK38_ANSWER_SCHEMA, validate as validate_eval_38
from .eval_39 import TASK39_ANSWER_SCHEMA, validate as validate_eval_39
from .eval_40 import TASK40_ANSWER_SCHEMA, validate as validate_eval_40

import inspect

TASK1_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the current username.",
    "properties": {
        "username": {
            "type": "string",
            "description": "The current username.",
        }
    },
    "required": ["username"],
    "additionalProperties": False,
}

def validate_task(task_id):
    """Wrapper to convert check function to validate function signature"""
    def wrapper(result=None, device_id=None, backup_dir=None):
        from .check_common import AppChecker
        checker = AppChecker(device_id)
        check_func = globals()[f'check_{task_id}']
        try:
            sig = inspect.signature(check_func)
            if 'result' in sig.parameters:
                passed = check_func(checker, result)
            else:
                passed = check_func(checker)
            return passed
        except Exception:
            return False
    return wrapper

SPOTIFY_TASKS = AppTasks(
    package_name="com.example.myspotify",
    task_items=[
        TaskItem(
            instruction="Check the current username",
            verify_func=validate_task(1),
            human_steps=2,
            is_reasoning=True,
            evaluation_type="hybrid",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the name of the currently playing song",
            verify_func=validate_eval_2,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Count how many categories are on the search page",
            verify_func=validate_eval_3,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Count how many songs are in the first recommended playlist in 'To get you started'",
            verify_func=validate_eval_4,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the title of the first podcast on the podcasts page",
            verify_func=validate_eval_5,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the publish date of the first podcast",
            verify_func=validate_eval_6,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK6_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the name of the first audiobook",
            verify_func=validate_eval_7,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK7_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the duration of the first audiobook",
            verify_func=validate_eval_8,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK8_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me who is the artist of the currently playing song",
            verify_func=validate_eval_9,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK9_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Play or pause the song on the full-screen playing page",
            verify_func=validate_task(10),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Play the next song",
            verify_func=validate_task(11),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Enter shuffle mode",
            verify_func=validate_task(12),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Enter repeat one mode",
            verify_func=validate_task(13),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Like the currently playing song",
            verify_func=validate_task(14),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Unlike the currently playing song",
            verify_func=validate_task(15),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Set the sleep timer to 15 minutes",
            verify_func=validate_task(16),
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Turn off the sleep timer",
            verify_func=validate_task(17),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="View the lyrics of IRIS OUT and tell me the first line",
            verify_func=validate_eval_18,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="View the credits of Style and tell me who is the lyricist",
            verify_func=validate_eval_19,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK19_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="View the artist information of Style and tell me the first sentence of the introduction",
            verify_func=validate_eval_20,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK20_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Search for the song 'Shape of You'",
            verify_func=validate_task(21),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Search for the song 'Perfect' and like it",
            verify_func=validate_task(22),
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a playlist 'My Jazz', search and add songs 'Shape of You' and 'Style'",
            verify_func=validate_task(23),
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Delete a recent search record on the search input page",
            verify_func=validate_task(24),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new playlist named 'My Rock' in the library",
            verify_func=validate_task(25),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Play the next song, enable shuffle mode, enable repeat one mode, and like the song",
            verify_func=validate_task(26),
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a playlist 'Workout', add the song 'In Your Eyes' and follow the artist of this song",
            verify_func=validate_task(27),
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Follow a new artist",
            verify_func=validate_task(28),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Follow a new podcast",
            verify_func=validate_task(29),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Randomly add a playlist to the library from the home page",
            verify_func=validate_task(30),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add a song to Liked Songs",
            verify_func=validate_task(31),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Search for the song 'Blank Space', like it, tell me the first line of the lyrics, view the credits and tell me who is the lyricist",
            verify_func=validate_eval_32,
            human_steps=9,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK32_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Proceed with premium subscription payment",
            verify_func=validate_task(33),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Tell me the title and publish date of the third podcast on the podcasts page, save it, post a comment 'Great episode!', and fast forward 15 seconds",
            verify_func=validate_eval_34,
            human_steps=8,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK34_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Fast forward a podcast by 15 seconds",
            verify_func=validate_task(35),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Unfollow Taylor Swift",
            verify_func=validate_task(36),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a playlist 'My Punk', search and add 'Shape of You', search and add 'Style', follow two new podcasts 'The Daily' and 'Crime Junkie'",
            verify_func=validate_task(37),
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Search for the song 'Style', like it, tell me the first line of the lyrics, view the credits and tell me who is the lyricist, then set the sleep timer to 15 minutes",
            verify_func=validate_eval_38,
            human_steps=13,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK38_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me how many songs are in the playlist 'Chill Vibes' in the library, if less than 6, add songs until there are 6",
            verify_func=validate_eval_39,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK39_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the title and publish date of the first audiobook, play and save it, post a comment 'Great episode!', fast forward 15 seconds, then save the second audiobook",
            verify_func=validate_eval_40,
            human_steps=12,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK40_ANSWER_SCHEMA,
        ),
    ],
)
