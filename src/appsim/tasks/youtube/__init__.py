from ..base import AppTasks, TaskItem

from .eval_1 import verify_watch_history_viewed
from .eval_2 import verify_first_search_result_liked_and_saved
from .eval_3 import verify_first_search_result_liked
from .eval_4 import verify_liked_video_played
from .eval_5 import verify_notifications_subscribed
from .eval_6 import verify_watch_later_video_deleted
from .eval_7 import verify_channel_subscribed
from .eval_8 import verify_channel_video_commented
from .eval_9 import verify_channel_watch_count, TASK9_ANSWER_SCHEMA
from .eval_10 import verify_liked_video_duration, TASK10_ANSWER_SCHEMA
from .eval_11 import verify_restricted_mode_state, TASK11_ANSWER_SCHEMA
from .eval_12 import verify_mentions_setting_state, TASK12_ANSWER_SCHEMA
from .eval_13 import verify_app_language_setting, TASK13_ANSWER_SCHEMA
from .eval_14 import verify_homepage_section_category_video_count, TASK14_ANSWER_SCHEMA
from .eval_15 import verify_search_result_count, TASK15_ANSWER_SCHEMA
from .eval_16 import verify_related_video_count, TASK16_ANSWER_SCHEMA
from .eval_17 import verify_first_video_comment_likes, TASK17_ANSWER_SCHEMA
from .eval_18 import verify_watch_later_total_duration, TASK18_ANSWER_SCHEMA
from .eval_19 import verify_liked_videos_total_duration, TASK19_ANSWER_SCHEMA
from .eval_20 import verify_channel_follower_count, TASK20_ANSWER_SCHEMA
from .eval_21 import verify_short_video_category_count, TASK21_ANSWER_SCHEMA
from .eval_22 import verify_short_video_subcategory_count, TASK22_ANSWER_SCHEMA
from .eval_23 import verify_short_video_category_likes_total, TASK23_ANSWER_SCHEMA
from .eval_24 import verify_short_video_category_duration_total, TASK24_ANSWER_SCHEMA
from .eval_25 import verify_latest_comment_likes, TASK25_ANSWER_SCHEMA
from .eval_26 import verify_watch_history_record_count, TASK26_ANSWER_SCHEMA
from .eval_27 import verify_mobile_network_video_quality, TASK27_ANSWER_SCHEMA
from .eval_28 import verify_wifi_video_quality, TASK28_ANSWER_SCHEMA
from .eval_29 import verify_homepage_all_category_video_count, TASK29_ANSWER_SCHEMA
from .eval_30 import verify_app_version, TASK30_ANSWER_SCHEMA
from .eval_31 import verify_video_playback_loop_and_volume_settings
from .eval_32 import verify_video_playback_quality_and_ambient_settings
from .eval_33 import verify_quality_setting_and_comment
from .eval_34 import verify_multiple_channel_videos_interacted_with
from .eval_35 import verify_external_video_interaction


YOUTUBE_TASKS = AppTasks(
    package_name="com.example.youtube_sim",
    task_items=[
        TaskItem(
            instruction='View my watch history',
            verify_func=verify_watch_history_viewed,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Search for apple, then like and save the first video',
            verify_func=verify_first_search_result_liked_and_saved,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to watch an ITX PC build video. Search for itx and like the first video',
            verify_func=verify_first_search_result_liked,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='View my liked videos, then play the song by the Chinese-language singer',
            verify_func=verify_liked_video_played,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Turn on the notification subscription button',
            verify_func=verify_notifications_subscribed,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Delete the last video in Watch later',
            verify_func=verify_watch_later_video_deleted,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Subscribe to Jay Chou',
            verify_func=verify_channel_subscribed,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Comment "This song is so beautiful" on Jay Chou 青花瓷',
            verify_func=verify_channel_video_commented,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='On the History page, check how many Jay Chou MVs I have watched in total',
            verify_func=verify_channel_watch_count,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK9_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check the duration of the first video in my liked videos',
            verify_func=verify_liked_video_duration,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK10_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check whether restricted mode is on or off',
            verify_func=verify_restricted_mode_state,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK11_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check whether the mentions button is on or off',
            verify_func=verify_mentions_setting_state,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK12_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check the current App language option',
            verify_func=verify_app_language_setting,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK13_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='On the Apple section of the Home page, how many videos are about phones?',
            verify_func=verify_homepage_section_category_video_count,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK14_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Search for iphone and check how many results this search has',
            verify_func=verify_search_result_count,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK15_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how many related videos are shown below the first video's playback page on the Home page",
            verify_func=verify_related_video_count,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK16_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='What is the total number of likes in the comments section of the first video on the Home page?',
            verify_func=verify_first_video_comment_likes,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK17_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check the total duration of the videos in Watch later',
            verify_func=verify_watch_later_total_duration,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check the total duration of the videos in Liked videos',
            verify_func=verify_liked_videos_total_duration,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK19_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check Jay Chou's follower count",
            verify_func=verify_channel_follower_count,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK20_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Scroll through Shorts. Among the first four shorts you see, how many are about computers?',
            verify_func=verify_short_video_category_count,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK21_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Scroll through Shorts. Among the first four shorts you see, how many are about mini PCs?',
            verify_func=verify_short_video_subcategory_count,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK22_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Scroll through Shorts. How many likes do the computer-related shorts among the first four shorts have in total?',
            verify_func=verify_short_video_category_likes_total,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK23_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Scroll through Shorts. Among the first four shorts you see, what is the total duration in seconds of the computer-related shorts? Reply with the number of seconds only',
            verify_func=verify_short_video_category_duration_total,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK24_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='In Jay Chou 夜曲 MV, how many likes does the newest comment have?',
            verify_func=verify_latest_comment_likes,
            human_steps=7,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='How many play records are in History?',
            verify_func=verify_watch_history_record_count,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK26_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check the option selected for Video quality on mobile networks',
            verify_func=verify_mobile_network_video_quality,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK27_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Check the option selected for Video quality on Wi-Fi',
            verify_func=verify_wifi_video_quality,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK28_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Among the first six videos under All on the Home page, how many are about computers?',
            verify_func=verify_homepage_all_category_video_count,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK29_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='What is the current app version number?',
            verify_func=verify_app_version,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK30_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Play Jay Chou 夜曲, choose Higher picture quality, and turn on Loop video and Stable volume',
            verify_func=verify_video_playback_loop_and_volume_settings,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Play Jay Chou 青花瓷, choose Higher picture quality, and turn off Ambient mode',
            verify_func=verify_video_playback_quality_and_ambient_settings,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='First turn on Higher picture quality on the Quality page, then play Jay Chou 青花瓷 and comment "This MV looks really clear"',
            verify_func=verify_quality_setting_and_comment,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Like, save, and comment "I have been a Jay Chou fan for ten years" on Jay Chou 夜曲, then like, save, and comment "This song reminds me of that girl" on 青花瓷',
            verify_func=verify_multiple_channel_videos_interacted_with,
            human_steps=24,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Like, save, and comment "Although your song sounds great, I still prefer listening to Jay Chou" on Taylor Swift\'s The Fate of Ophelia',
            verify_func=verify_external_video_interaction,
            human_steps=11,
            is_reasoning=False,
        ),
    ],
)
