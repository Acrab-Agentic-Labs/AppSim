# 引用所有检验函数
from ..base import AppTasks, TaskItem
from .eval_1 import TASK1_ANSWER_SCHEMA, verify_current_username
from .eval_2 import TASK2_ANSWER_SCHEMA, verify_playlist_with_most_songs
from .eval_3 import verify_first_song_deleted_from_playlist
from .eval_4 import verify_current_song_playing
from .eval_5 import verify_current_song_paused
from .eval_6 import verify_previous_song_played
from .eval_7 import verify_shuffle_mode_enabled
from .eval_8 import verify_current_song_favorited
from .eval_9 import verify_volume_adjusted
from .eval_10 import verify_search_playback_favorite_lyrics_next_shuffle
from .eval_11 import verify_first_daily_recommendation_played
from .eval_12 import verify_playlist_created_with_song
from .eval_13 import verify_searched_song_played
from .eval_14 import verify_artist_song_played
from .eval_15 import verify_song_detail_viewed
from .eval_16 import verify_song_lyrics_shown
from .eval_17 import verify_playback_scene_set
from .eval_18 import TASK18_ANSWER_SCHEMA, verify_first_ranked_song_name_reported
from .eval_19 import verify_ranked_song_played
from .eval_20 import verify_playlist_collected
from .eval_21 import verify_playlist_song_deleted
from .eval_22 import verify_listening_stats_viewed
from .eval_23 import verify_song_unfavorited
from .eval_24 import verify_playlist_comment_posted
from .eval_25 import TASK25_ANSWER_SCHEMA, verify_search_playback_favorite_lyrics_mv
from .eval_26 import verify_song_recognition_attempted
from .eval_27 import verify_playlist_sort_order_changed
from .eval_28 import verify_album_collected
from .eval_29 import verify_artist_unfollowed
from .eval_30 import verify_artist_mv_playing
from .eval_31 import verify_player_style_changed
from .eval_32 import TASK32_ANSWER_SCHEMA, verify_first_song_comment_time_reported
from .eval_33 import TASK33_ANSWER_SCHEMA, verify_favorite_song_count
from .eval_34 import TASK34_ANSWER_SCHEMA, verify_third_song_comment_content_reported
from .eval_35 import TASK35_ANSWER_SCHEMA, verify_song_playback_favorite_lyrics_style_playlist
from .eval_36 import TASK36_ANSWER_SCHEMA, verify_fan_count
from .eval_37 import TASK37_ANSWER_SCHEMA, verify_target_playlist_song_count
from .eval_38 import TASK38_ANSWER_SCHEMA, verify_playlist_song_actions_and_genre
from .eval_39 import TASK39_ANSWER_SCHEMA, verify_playlist_song_actions_lyrics_and_listening_stats

# 所有指令
MUSIC_TASKS = AppTasks(
    package_name="com.example.netease_cloud_music_sim",
    task_items=[
        TaskItem(
            instruction="告诉我用户名是什么",
            verify_func=verify_current_username,
            human_steps=1,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="在'我的'页面的所有歌单中哪一个歌单里的歌曲数量最多",
            verify_func=verify_playlist_with_most_songs,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="删除'我的'页面中热歌榜歌单的第一首歌曲",
            verify_func=verify_first_song_deleted_from_playlist,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放当前歌曲",
            verify_func=verify_current_song_playing,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="暂停播放当前的歌曲",
            verify_func=verify_current_song_paused,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="切换播放上一首歌曲",
            verify_func=verify_previous_song_played,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将播放模式改为随机播放",
            verify_func=verify_shuffle_mode_enabled,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="收藏当前歌曲",
            verify_func=verify_current_song_favorited,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="调节当前音乐播放的音量",
            verify_func=verify_volume_adjusted,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'丑八怪'并播放，收藏该歌曲，查看歌词，然后切换到下一首歌曲，并设置为随机播放模式",
            verify_func=verify_search_playback_favorite_lyrics_next_shuffle,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放'每日推荐'中的第一首歌曲",
            verify_func=verify_first_daily_recommendation_played,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="创建一个新的歌单,并添加一首音乐",
            verify_func=verify_playlist_created_with_song,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'稻香'并播放第一首搜索结果",
            verify_func=verify_searched_song_played,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索一个歌手，进入歌手主页，播放第一首歌",
            verify_func=verify_artist_song_played,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="点击当前播放的歌曲，查看歌曲百科",
            verify_func=verify_song_detail_viewed,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看一首歌曲的歌词",
            verify_func=verify_song_lyrics_shown,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='漫游播放并设置播放场景为"欢快"',
            verify_func=verify_playback_scene_set,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入排行榜的新歌榜,告诉我第一首歌名称",
            verify_func=verify_first_ranked_song_name_reported,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="在排行榜中打开一个榜单并播放第一首歌曲",
            verify_func=verify_ranked_song_played,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='在推荐歌单中收藏歌单"怀旧金曲"',
            verify_func=verify_playlist_collected,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='删除歌单"新歌榜"中的第一首歌',
            verify_func=verify_playlist_song_deleted,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看每周、每月听歌时长",
            verify_func=verify_listening_stats_viewed,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='取消收藏"晴天"',
            verify_func=verify_song_unfavorited,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="在歌单中选择一首歌曲并发表评论",
            verify_func=verify_playlist_comment_posted,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'薛之谦'，进入歌手主页，播放\"演员\"，收藏该歌曲，查看歌词并告诉我第一句歌词，并播放MV",
            verify_func=verify_search_playback_favorite_lyrics_mv,
            human_steps=17,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="使用听歌识曲功能识别一首歌曲",
            verify_func=verify_song_recognition_attempted,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='更改"我喜欢的音乐"的排序顺序',
            verify_func=verify_playlist_sort_order_changed,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索歌手周杰伦,在歌手主页选择一个专辑并收藏",
            verify_func=verify_album_collected,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将关注列表中的一位歌手删除",
            verify_func=verify_artist_unfollowed,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索一位歌手，进入歌手主页播放一个MV",
            verify_func=verify_artist_mv_playing,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="更改播放器样式",
            verify_func=verify_player_style_changed,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='告诉我"晴天"的第一条评论的发布时间',
            verify_func=verify_first_song_comment_time_reported,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK32_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='数一下"我喜欢的音乐"里有几首歌曲',
            verify_func=verify_favorite_song_count,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK33_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='告诉我"七里香"的第三条评论是什么',
            verify_func=verify_third_song_comment_content_reported,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK34_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="搜索'倔强'并播放，收藏该歌曲，查看歌词并告诉我第一句，更改播放器样式，然后创建一个新歌单并添加该歌曲",
            verify_func=verify_song_playback_favorite_lyrics_style_playlist,
            human_steps=20,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK35_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="数一下我的粉丝数目",
            verify_func=verify_fan_count,
            human_steps=1,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK36_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='数一下"热歌榜"里有多少首歌曲',
            verify_func=verify_target_playlist_song_count,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK37_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='收藏歌单"国风榜"，并播放"青花瓷"，收藏歌曲，发布评论"真好听"，查看歌曲百科并告诉我曲风是什么',
            verify_func=verify_playlist_song_actions_and_genre,
            human_steps=13,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK38_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='收藏歌单"ACG榜"，并播放"夜曲"，收藏歌曲，查看歌词并告诉我第一句歌词是什么，然后查看一下这周的听歌时长',
            verify_func=verify_playlist_song_actions_lyrics_and_listening_stats,
            human_steps=11,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK39_ANSWER_SCHEMA,
        ),
    ],
)
