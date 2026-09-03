from ..base import AppTasks, NumericReasoningCategory, TaskItem
from .eval_1 import verify_current_username
from .eval_10 import verify_full_screen_playback_state
from .eval_11 import verify_next_song_played
from .eval_12 import verify_shuffle_mode_enabled
from .eval_13 import verify_repeat_one_mode_enabled
from .eval_14 import verify_current_song_liked
from .eval_15 import verify_current_song_unliked
from .eval_16 import verify_sleep_timer_set
from .eval_17 import verify_sleep_timer_disabled
from .eval_21 import verify_song_search
from .eval_22 import verify_searched_song_liked
from .eval_23 import verify_playlist_created_with_songs
from .eval_24 import verify_recent_search_deleted
from .eval_25 import verify_playlist_created
from .eval_26 import verify_playback_controls_and_like
from .eval_27 import verify_playlist_created_and_artist_followed
from .eval_28 import verify_new_artist_followed
from .eval_29 import verify_new_podcast_followed
from .eval_30 import verify_playlist_added_to_library
from .eval_31 import verify_song_added_to_liked_songs
from .eval_33 import verify_premium_subscription_activated
from .eval_35 import verify_podcast_fast_forwarded
from .eval_36 import verify_artist_unfollowed
from .eval_37 import verify_playlist_created_and_podcasts_followed
from .eval_2 import TASK2_ANSWER_SCHEMA, verify_current_playing_song_name
from .eval_3 import TASK3_ANSWER_SCHEMA, verify_search_page_category_count
from .eval_4 import TASK4_ANSWER_SCHEMA, verify_first_recommended_playlist_song_count
from .eval_5 import TASK5_ANSWER_SCHEMA, verify_first_podcast_title
from .eval_6 import TASK6_ANSWER_SCHEMA, verify_first_podcast_publish_date
from .eval_7 import TASK7_ANSWER_SCHEMA, verify_first_audiobook_name
from .eval_8 import TASK8_ANSWER_SCHEMA, verify_first_audiobook_duration
from .eval_9 import TASK9_ANSWER_SCHEMA, verify_current_playing_song_artist_name
from .eval_18 import TASK18_ANSWER_SCHEMA, verify_iris_out_first_lyrics_line
from .eval_19 import TASK19_ANSWER_SCHEMA, verify_style_lyricist
from .eval_20 import TASK20_ANSWER_SCHEMA, verify_style_artist_intro_first_sentence
from .eval_32 import TASK32_ANSWER_SCHEMA, verify_blank_space_first_lyrics_line_and_lyricist
from .eval_34 import TASK34_ANSWER_SCHEMA, verify_third_podcast_title_and_publish_date
from .eval_38 import TASK38_ANSWER_SCHEMA, verify_style_first_lyrics_line_and_lyricist
from .eval_39 import TASK39_ANSWER_SCHEMA, verify_chill_vibes_initial_song_count
from .eval_40 import TASK40_ANSWER_SCHEMA, verify_first_audiobook_title_and_publish_date

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

def build_spotify_verify_func(check_func):
    """Wrapper to convert check function to validate function signature"""
    def wrapper(result=None, device_id=None, backup_dir=None):
        from .check_common import AppChecker
        checker = AppChecker(device_id)
        try:
            sig = inspect.signature(check_func)
            if 'result' in sig.parameters:
                passed = check_func(checker, result)
            else:
                passed = check_func(checker)
            return passed
        except Exception:
            return False
    wrapper.__name__ = check_func.__name__
    return wrapper

SPOTIFY_TASKS = AppTasks(
    package_name="com.example.myspotify",
    task_items=[
        TaskItem(
            instruction="Check the current username",
            verify_func=build_spotify_verify_func(verify_current_username),
            human_steps=2,
            evaluation_type="hybrid",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the name of the currently playing song",
            verify_func=verify_current_playing_song_name,
            human_steps=2,
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Count how many categories are on the search page",
            verify_func=verify_search_page_category_count,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Count how many songs are in the first recommended playlist in 'To get you started'",
            verify_func=verify_first_recommended_playlist_song_count,
            human_steps=2,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the title of the first podcast on the podcasts page",
            verify_func=verify_first_podcast_title,
            human_steps=2,
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the publish date of the first podcast",
            verify_func=verify_first_podcast_publish_date,
            human_steps=2,
            evaluation_type="answer",
            answer_schema=TASK6_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the name of the first audiobook",
            verify_func=verify_first_audiobook_name,
            human_steps=2,
            evaluation_type="answer",
            answer_schema=TASK7_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the duration of the first audiobook",
            verify_func=verify_first_audiobook_duration,
            human_steps=3,
            evaluation_type="answer",
            answer_schema=TASK8_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me who is the artist of the currently playing song",
            verify_func=verify_current_playing_song_artist_name,
            human_steps=3,
            evaluation_type="answer",
            answer_schema=TASK9_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Play or pause the song on the full-screen playing page",
            verify_func=build_spotify_verify_func(verify_full_screen_playback_state),
            human_steps=3,
        ),
        TaskItem(
            instruction="Play the next song",
            verify_func=build_spotify_verify_func(verify_next_song_played),
            human_steps=3,
        ),
        TaskItem(
            instruction="Enter shuffle mode",
            verify_func=build_spotify_verify_func(verify_shuffle_mode_enabled),
            human_steps=4,
        ),
        TaskItem(
            instruction="Enter repeat one mode",
            verify_func=build_spotify_verify_func(verify_repeat_one_mode_enabled),
            human_steps=4,
        ),
        TaskItem(
            instruction="Like the currently playing song",
            verify_func=build_spotify_verify_func(verify_current_song_liked),
            human_steps=4,
        ),
        TaskItem(
            instruction="Unlike the currently playing song",
            verify_func=build_spotify_verify_func(verify_current_song_unliked),
            human_steps=3,
        ),
        TaskItem(
            instruction="Set the sleep timer to 15 minutes",
            verify_func=build_spotify_verify_func(verify_sleep_timer_set),
            human_steps=5,
        ),
        TaskItem(
            instruction="Turn off the sleep timer",
            verify_func=build_spotify_verify_func(verify_sleep_timer_disabled),
            human_steps=4,
        ),
        TaskItem(
            instruction="View the lyrics of IRIS OUT and tell me the first line",
            verify_func=verify_iris_out_first_lyrics_line,
            human_steps=3,
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="View the credits of Style and tell me who is the lyricist",
            verify_func=verify_style_lyricist,
            human_steps=4,
            evaluation_type="answer",
            answer_schema=TASK19_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="View the artist information of Style and tell me the first sentence of the introduction",
            verify_func=verify_style_artist_intro_first_sentence,
            human_steps=4,
            evaluation_type="answer",
            answer_schema=TASK20_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Search for the song 'Shape of You'",
            verify_func=build_spotify_verify_func(verify_song_search),
            human_steps=3,
        ),
        TaskItem(
            instruction="Search for the song 'Perfect' and like it",
            verify_func=build_spotify_verify_func(verify_searched_song_liked),
            human_steps=6,
        ),
        TaskItem(
            instruction="Create a playlist 'My Jazz', search and add songs 'Shape of You' and 'Style'",
            verify_func=build_spotify_verify_func(verify_playlist_created_with_songs),
            human_steps=11,
        ),
        TaskItem(
            instruction="Delete a recent search record on the search input page",
            verify_func=build_spotify_verify_func(verify_recent_search_deleted),
            human_steps=2,
        ),
        TaskItem(
            instruction="Create a new playlist named 'My Rock' in the library",
            verify_func=build_spotify_verify_func(verify_playlist_created),
            human_steps=2,
        ),
        TaskItem(
            instruction="Play the next song, enable shuffle mode, enable repeat one mode, and like the song",
            verify_func=build_spotify_verify_func(verify_playback_controls_and_like),
            human_steps=6,
        ),
        TaskItem(
            instruction="Create a playlist 'Workout', add the song 'In Your Eyes' and follow the artist of this song",
            verify_func=build_spotify_verify_func(verify_playlist_created_and_artist_followed),
            human_steps=12,
        ),
        TaskItem(
            instruction="Follow a new artist",
            verify_func=build_spotify_verify_func(verify_new_artist_followed),
            human_steps=2,
        ),
        TaskItem(
            instruction="Follow a new podcast",
            verify_func=build_spotify_verify_func(verify_new_podcast_followed),
            human_steps=3,
        ),
        TaskItem(
            instruction="Randomly add a playlist to the library from the home page",
            verify_func=build_spotify_verify_func(verify_playlist_added_to_library),
            human_steps=3,
        ),
        TaskItem(
            instruction="Add a song to Liked Songs",
            verify_func=build_spotify_verify_func(verify_song_added_to_liked_songs),
            human_steps=3,
        ),
        TaskItem(
            instruction="Search for the song 'Blank Space', like it, tell me the first line of the lyrics, view the credits and tell me who is the lyricist",
            verify_func=verify_blank_space_first_lyrics_line_and_lyricist,
            human_steps=9,
            evaluation_type="answer",
            answer_schema=TASK32_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Proceed with premium subscription payment",
            verify_func=build_spotify_verify_func(verify_premium_subscription_activated),
            human_steps=4,
        ),
        TaskItem(
            instruction="Tell me the title and publish date of the third podcast on the podcasts page, save it, post a comment 'Great episode!', and fast forward 15 seconds",
            verify_func=verify_third_podcast_title_and_publish_date,
            human_steps=8,
            evaluation_type="answer",
            answer_schema=TASK34_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Fast forward a podcast by 15 seconds",
            verify_func=build_spotify_verify_func(verify_podcast_fast_forwarded),
            human_steps=3,
        ),
        TaskItem(
            instruction="Unfollow Taylor Swift",
            verify_func=build_spotify_verify_func(verify_artist_unfollowed),
            human_steps=3,
        ),
        TaskItem(
            instruction="Create a playlist 'My Punk', search and add 'Shape of You', search and add 'Style', follow two new podcasts 'The Daily' and 'Crime Junkie'",
            verify_func=build_spotify_verify_func(verify_playlist_created_and_podcasts_followed),
            human_steps=15,
        ),
        TaskItem(
            instruction="Search for the song 'Style', like it, tell me the first line of the lyrics, view the credits and tell me who is the lyricist, then set the sleep timer to 15 minutes",
            verify_func=verify_style_first_lyrics_line_and_lyricist,
            human_steps=13,
            evaluation_type="answer",
            answer_schema=TASK38_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me how many songs are in the playlist 'Chill Vibes' in the library, if less than 6, add songs until there are 6",
            verify_func=verify_chill_vibes_initial_song_count,
            human_steps=6,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COUNT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK39_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the title and publish date of the first audiobook, play and save it, post a comment 'Great episode!', fast forward 15 seconds, then save the second audiobook",
            verify_func=verify_first_audiobook_title_and_publish_date,
            human_steps=12,
            evaluation_type="answer",
            answer_schema=TASK40_ANSWER_SCHEMA,
        ),
    ],
)
