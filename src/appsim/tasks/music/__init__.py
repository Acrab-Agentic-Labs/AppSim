# 引用所有检验函数
from ..base import AppTasks, TaskItem
from .test_task_01 import TASK1_ANSWER_SCHEMA, check_username_is_reported
from .test_task_02 import TASK2_ANSWER_SCHEMA, find_playlist_with_most_songs
from .test_task_03 import check_delete_song_from_hot_playlist
from .test_task_04 import check_current_song_is_playing
from .test_task_05 import check_is_paused
from .test_task_06 import check_switch_to_previous_song
from .test_task_07 import check_shuffle_mode_enabled
from .test_task_08 import check_song_is_favorited
from .test_task_09 import check_volume_is_adjusted
from .test_task_10 import check_composite_search_play_favorite_lyrics_next_shuffle
from .test_task_11 import check_play_first_daily_recommendation
from .test_task_12 import check_create_playlist_and_add_song
from .test_task_13 import check_search_and_play_song
from .test_task_14 import check_search_artist_and_play
from .test_task_15 import check_view_song_detail
from .test_task_16 import check_lyrics_are_shown
from .test_task_17 import check_stroll_scene_is_set
from .test_task_18 import TASK18_ANSWER_SCHEMA, check_first_song_name_is_reported
from .test_task_19 import check_play_from_rank_list
from .test_task_20 import check_playlist_is_collected
from .test_task_21 import check_song_is_deleted_from_playlist
from .test_task_22 import check_listening_stats_is_viewed
from .test_task_23 import check_song_is_unfavorited
from .test_task_24 import check_comment_is_posted
from .test_task_25 import TASK25_ANSWER_SCHEMA, check_composite_xuezhiqian_play_favorite_lyrics_mv
from .test_task_26 import check_song_recognition_is_attempted
from .test_task_27 import check_playlist_sort_order_is_changed
from .test_task_28 import check_album_is_collected
from .test_task_29 import check_artist_is_unfollowed
from .test_task_30 import check_mv_is_playing
from .test_task_31 import check_player_style_is_changed
from .test_task_32 import TASK32_ANSWER_SCHEMA, check_first_comment_time_reported
from .test_task_33 import TASK33_ANSWER_SCHEMA, check_favorite_song_count
from .test_task_34 import TASK34_ANSWER_SCHEMA, check_third_comment_content_reported
from .test_task_35 import TASK35_ANSWER_SCHEMA, check_composite_juejiang_full
from .test_task_36 import TASK36_ANSWER_SCHEMA, check_fan_count
from .test_task_37 import TASK37_ANSWER_SCHEMA, check_hot_rank_song_count
from .test_task_38 import TASK38_ANSWER_SCHEMA, check_composite_guofeng_qinghuaci
from .test_task_39 import TASK39_ANSWER_SCHEMA, check_composite_acg_yequ

# 所有指令
MUSIC_TASKS = AppTasks(
    package_name="com.example.netease_cloud_music_sim",
    task_items=[
        TaskItem(
            instruction="告诉我用户名是什么",
            verify_func=check_username_is_reported,
            human_steps=1,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="在'我的'页面的所有歌单中哪一个歌单里的歌曲数量最多",
            verify_func=find_playlist_with_most_songs,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="删除'我的'页面中热歌榜歌单的第一首歌曲",
            verify_func=check_delete_song_from_hot_playlist,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放当前歌曲",
            verify_func=check_current_song_is_playing,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="暂停播放当前的歌曲",
            verify_func=check_is_paused,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="切换播放上一首歌曲",
            verify_func=check_switch_to_previous_song,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将播放模式改为随机播放",
            verify_func=check_shuffle_mode_enabled,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="收藏当前歌曲",
            verify_func=check_song_is_favorited,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="调节当前音乐播放的音量",
            verify_func=check_volume_is_adjusted,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'丑八怪'并播放，收藏该歌曲，查看歌词，然后切换到下一首歌曲，并设置为随机播放模式",
            verify_func=check_composite_search_play_favorite_lyrics_next_shuffle,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放'每日推荐'中的第一首歌曲",
            verify_func=check_play_first_daily_recommendation,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="创建一个新的歌单,并添加一首音乐",
            verify_func=check_create_playlist_and_add_song,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'稻香'并播放第一首搜索结果",
            verify_func=check_search_and_play_song,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索一个歌手，进入歌手主页，播放第一首歌",
            verify_func=check_search_artist_and_play,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="点击当前播放的歌曲，查看歌曲百科",
            verify_func=check_view_song_detail,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看一首歌曲的歌词",
            verify_func=check_lyrics_are_shown,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='漫游播放并设置播放场景为"欢快"',
            verify_func=check_stroll_scene_is_set,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入排行榜的新歌榜,告诉我第一首歌名称",
            verify_func=check_first_song_name_is_reported,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="在排行榜中打开一个榜单并播放第一首歌曲",
            verify_func=check_play_from_rank_list,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='在推荐歌单中收藏歌单"怀旧金曲"',
            verify_func=check_playlist_is_collected,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='删除歌单"新歌榜"中的第一首歌',
            verify_func=check_song_is_deleted_from_playlist,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看每周、每月听歌时长",
            verify_func=check_listening_stats_is_viewed,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='取消收藏"晴天"',
            verify_func=check_song_is_unfavorited,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="在歌单中选择一首歌曲并发表评论",
            verify_func=check_comment_is_posted,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'薛之谦'，进入歌手主页，播放\"演员\"，收藏该歌曲，查看歌词并告诉我第一句歌词，并播放MV",
            verify_func=check_composite_xuezhiqian_play_favorite_lyrics_mv,
            human_steps=17,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="使用听歌识曲功能识别一首歌曲",
            verify_func=check_song_recognition_is_attempted,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='更改"我喜欢的音乐"的排序顺序',
            verify_func=check_playlist_sort_order_is_changed,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索歌手周杰伦,在歌手主页选择一个专辑并收藏",
            verify_func=check_album_is_collected,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将关注列表中的一位歌手删除",
            verify_func=check_artist_is_unfollowed,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索一位歌手，进入歌手主页播放一个MV",
            verify_func=check_mv_is_playing,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="更改播放器样式",
            verify_func=check_player_style_is_changed,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='告诉我"晴天"的第一条评论的发布时间',
            verify_func=check_first_comment_time_reported,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK32_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='数一下"我喜欢的音乐"里有几首歌曲',
            verify_func=check_favorite_song_count,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK33_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='告诉我"七里香"的第三条评论是什么',
            verify_func=check_third_comment_content_reported,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK34_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="搜索'倔强'并播放，收藏该歌曲，查看歌词并告诉我第一句，更改播放器样式，然后创建一个新歌单并添加该歌曲",
            verify_func=check_composite_juejiang_full,
            human_steps=20,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK35_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="数一下我的粉丝数目",
            verify_func=check_fan_count,
            human_steps=1,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK36_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='数一下"热歌榜"里有多少首歌曲',
            verify_func=check_hot_rank_song_count,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK37_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='收藏歌单"国风榜"，并播放"青花瓷"，收藏歌曲，发布评论"真好听"，查看歌曲百科并告诉我曲风是什么',
            verify_func=check_composite_guofeng_qinghuaci,
            human_steps=13,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK38_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='收藏歌单"ACG榜"，并播放"夜曲"，收藏歌曲，查看歌词并告诉我第一句歌词是什么，然后查看一下这周的听歌时长',
            verify_func=check_composite_acg_yequ,
            human_steps=11,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK39_ANSWER_SCHEMA,
        ),
    ],
)
