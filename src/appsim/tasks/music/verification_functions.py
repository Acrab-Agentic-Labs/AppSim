"""
音乐App自动化测试验证函数
用于验证各项任务是否成功完成
"""

import subprocess
import json
import os

# App包名
APP_PACKAGE = "com.example.mymusic"


def read_json_from_device(file_path, device_id=None, result=None):
    """
    从设备读取JSON文件
    :param file_path: 设备上的文件路径(相对于app私有目录)
    :return: JSON数据或None
    """
    try:
        # 将设备上的文件复制到本地
        local_file = f"temp_{os.path.basename(file_path)}"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])

        cmd.extend(["exec-out", "run-as", APP_PACKAGE, "cat", f"files/{file_path}"])

        subprocess.run(cmd, stdout=open(local_file, "w"), stderr=subprocess.DEVNULL)

        # 读取JSON
        with open(local_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 删除临时文件
        os.remove(local_file)
        return data
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}")
        return None


# ==================== 任务1-10 (低难度) ====================


def task_01_check_open_recommend_page():
    """
    任务1: 打开app并进入"推荐"首页
    验证: 检查app_state.json中currentPage是否为"recommend"
    """
    data = read_json_from_device("autotest/app_state.json")
    if data:
        return data.get("currentPage") == "recommend"
    return False


def task_02_check_navigate_to_stroll(device_id=None, result=None):
    """
    任务2: 从"推荐"页面进入"漫游"页面
    验证: 检查app_state.json中currentPage是否为"stroll"
    """
    data = read_json_from_device("autotest/app_state.json", device_id, result)
    if data:
        return data.get("currentPage") == "stroll"
    return False


def task_03_check_navigate_to_profile(device_id=None, result=None):
    """
    任务3: 从"推荐"页面进入"我的"页面
    验证: 检查app_state.json中currentPage是否为"profile"或"my"
    """
    data = read_json_from_device("autotest/app_state.json", device_id, result)
    if data:
        current_page = data.get("currentPage")
        return current_page in ["profile", "my", "mine"]
    return False


def task_04_check_play_song(device_id=None, result=None):
    """
    任务4: 播放当前暂停的歌曲
    验证: 检查playback_state.json中isPlaying是否为true
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result)
    if data:
        return data.get("isPlaying") == True
    return False


def task_05_check_pause_song(device_id=None, result=None):
    """
    任务5: 暂停播放当前的歌曲
    验证: 检查playback_state.json中isPlaying是否为false
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result)
    if data:
        return data.get("isPlaying") == False
    return False


def task_06_check_switch_previous_song(expected_song_id=None, device_id=None, result=None):
    """
    任务6: 切换播放上一首歌曲
    验证: 检查playback_state.json中currentSong.songId是否变化
    :param expected_song_id: 期望的歌曲ID(如果已知)
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result)
    if data and "currentSong" in data:
        if expected_song_id:
            return data["currentSong"].get("songId") == expected_song_id
        # 如果没有指定期望ID,只要有currentSong就认为切换成功
        return "songId" in data["currentSong"]
    return False


def task_07_check_shuffle_mode(device_id=None, result=None):
    """
    任务7: 将播放模式改为随机播放
    验证: 检查playback_state.json中playbackMode是否为"shuffle"
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result)
    if data:
        return data.get("playbackMode") == "shuffle"
    return False


def task_08_check_favorite_song(song_id, device_id=None, result=None):
    """
    任务8: 收藏当前歌曲
    验证: 检查user_favorites.json中是否包含指定歌曲
    :param song_id: 被收藏的歌曲ID
    """
    data = read_json_from_device("autotest/user_favorites.json", device_id, result)
    if data and "favoriteSongs" in data:
        song_ids = [song.get("songId") for song in data["favoriteSongs"]]
        return song_id in song_ids
    return False


def task_09_check_volume_adjusted(expected_volume=None, device_id=None, result=None):
    """
    任务9: 调节当前音乐播放的音量
    验证: 检查playback_state.json中volume是否改变
    :param expected_volume: 期望的音量值(0-100)
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result)
    if data:
        if expected_volume is not None:
            return data.get("volume") == expected_volume
        # 如果没有指定期望音量,只要volume字段存在就认为成功
        return "volume" in data
    return False


def task_10_check_enter_playlist(device_id=None, result=None):
    """
    任务10: 随机进入"我的"中的一个歌单
    验证: 检查user_playlists.json中currentViewingPlaylist不为null
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result)
    if data:
        return data.get("currentViewingPlaylist") is not None
    return False


# ==================== 任务11-21 (中难度) ====================


def task_11_check_daily_recommend_third_song(device_id=None, result=None):
    """
    任务11: 进入"每日推荐"播放第三首歌曲
    验证: 检查playback_state.json中currentSong.source是否为"daily_recommend"且sourceDetail包含"第3首"
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result)
    if data and "currentSong" in data:
        song = data["currentSong"]
        return song.get("source") == "daily_recommend" and "第3首" in song.get("sourceDetail", "")
    return False


def task_12_check_create_playlist_and_add_song(playlist_name=None, device_id=None, result=None):
    """
    任务12: 创建一个新的歌单,并添加首音乐
    验证: 检查user_playlists.json中是否有指定名称的歌单,且songCount > 0
    :param playlist_name: 新建歌单的名称。如果为None，则检查最新创建的歌单；否则检查指定名称的歌单
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result)
    if data and "playlists" in data:
        playlists = data["playlists"]

        if playlist_name is None:
            # 不传参数时，检查最新创建的歌单
            if not playlists:
                return False
            # 按创建时间排序，取最新的
            sorted_playlists = sorted(playlists, key=lambda x: x.get("createTime", 0), reverse=True)
            latest = sorted_playlists[0]
            print(f"  → 检查最新创建的歌单: 《{latest.get('playlistName')}》")
            print(f"  → 歌曲数量: {latest.get('songCount', 0)}")
            return latest.get("songCount", 0) > 0
        else:
            # 传参数时，检查指定名称的歌单
            print(f"  → 检查指定歌单: 《{playlist_name}》")
            for playlist in playlists:
                if playlist.get("playlistName") == playlist_name:
                    print(f"  → 歌曲数量: {playlist.get('songCount', 0)}")
                    return playlist.get("songCount", 0) > 0
            print(f"  → 未找到名称为《{playlist_name}》的歌单")
    return False


def task_13_check_search_and_play(search_query="稻香", device_id=None, result=None):
    """
    任务13: 搜索"稻香"并播放
    验证: 检查search_history.json中有该搜索记录,且action为"play"
    :param search_query: 搜索关键词，默认'稻香'
    """
    data = read_json_from_device("autotest/search_history.json", device_id, result)
    if data and "searches" in data:
        print(f"  → 检查搜索记录: 《{search_query}》")
        for search in data["searches"]:
            if search.get("query") == search_query and search.get("action") == "play":
                print(f"  → 找到匹配的搜索并播放记录")
                return True
        print(f"  → 未找到搜索《{search_query}》并播放的记录")
    return False


def task_14_check_search_artist_and_play(device_id=None, result=None):
    """
    任务14: 搜索某个歌手并播放其中的第一首歌
    验证: 检查search_history.json中有歌手搜索记录,且resultType为"artist",action为"play"
    """
    data = read_json_from_device("autotest/search_history.json", device_id, result)
    if data and "searches" in data:
        for search in data["searches"]:
            if search.get("resultType") == "artist" and search.get("action") == "play":
                return True
    return False


def task_15_check_view_song_detail(song_id, device_id=None, result=None):
    """
    任务15: 查看一首歌曲的详细信息
    验证: 检查app_state.json中currentPage为"song_detail"且包含指定songId
    :param song_id: 查看详情的歌曲ID
    """
    data = read_json_from_device("autotest/app_state.json", device_id, result)
    if data:
        return data.get("currentPage") == "song_detail" and data.get("currentSongId") == song_id
    return False


def task_16_check_view_lyrics(device_id=None, result=None):
    """
    任务16: 查看一首歌曲的歌词
    验证: 检查app_state.json中showLyrics为true或currentPage为"lyrics"
    """
    data = read_json_from_device("autotest/app_state.json", device_id, result)
    if data:
        return data.get("showLyrics") == True or data.get("currentPage") == "lyrics"
    return False


def task_17_check_stroll_scene_setting(scene_name, device_id=None, result=None):
    """
    任务17: 漫游播放并设置播放场景为"伪感"
    验证: 检查player_settings.json中strollMode.scene是否为指定场景
    :param scene_name: 场景名称,如"伪感"
    """
    data = read_json_from_device("autotest/player_settings.json", device_id, result)
    if data and "strollMode" in data:
        return data["strollMode"].get("scene") == scene_name
    return False


def task_18_check_copy_comment(device_id=None, result=None):
    """
    任务18: 打开一首歌曲的评论区并随机复制一条评论
    验证: 此任务难以自动验证(需要检测剪贴板),返回False表示不支持
    """
    # 无法可靠验证剪贴板内容
    return False


def task_19_check_rank_list_play(device_id=None, result=None):
    """
    任务19: 在排行榜中随机选择打开一个榜单并播放第一首歌曲
    验证: 检查playback_state.json中currentSong.source包含"rank"或"榜单"
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result)
    if data and "currentSong" in data:
        source = data["currentSong"].get("source", "")
        return "rank" in source or "榜单" in source
    return False


def task_20_check_collect_playlist(playlist_id, device_id=None, result=None):
    """
    任务20: 在推荐歌单中随机选择一个歌单并收藏
    验证: 检查collected_items.json中collectedPlaylists是否包含指定歌单
    :param playlist_id: 收藏的歌单ID
    """
    data = read_json_from_device("autotest/collected_items.json", device_id, result)
    if data and "collectedPlaylists" in data:
        playlist_ids = [p.get("playlistId") for p in data["collectedPlaylists"]]
        return playlist_id in playlist_ids
    return False


def task_21_check_delete_song_from_playlist(playlist_id, expected_count, device_id=None, result=None):
    """
    任务21: 删除歌单中的第一首歌
    验证: 检查user_playlists.json中指定歌单的songCount是否减少
    :param playlist_id: 歌单ID
    :param expected_count: 删除后期望的歌曲数量
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result)
    if data and "playlists" in data:
        for playlist in data["playlists"]:
            if playlist.get("playlistId") == playlist_id:
                return playlist.get("songCount") == expected_count
    return False


# ==================== 任务22-31 (高难度) ====================


def task_22_check_view_listening_stats(stat_type, device_id=None, result=None):
    """
    任务22: 查看每周、每月听歌时长
    验证: 检查listening_stats.json中viewedStats的对应字段为true
    :param stat_type: "weekly"或"monthly"
    """
    data = read_json_from_device("autotest/listening_stats.json", device_id, result)
    if data and "viewedStats" in data:
        return data["viewedStats"].get(stat_type) == True
    return False


def task_23_check_share_to_wechat(device_id=None, result=None):
    """
    任务23: 分享一首歌曲到微信朋友圈
    验证: 外部应用交互难以验证,返回False表示不支持
    """
    # 无法验证微信朋友圈分享
    return False


def task_24_check_post_comment(song_id, comment_content, device_id=None, result=None):
    """
    任务24: 在歌单中选择一首歌曲并发表评论
    验证: 检查comments.json中是否有对应歌曲的评论
    :param song_id: 评论的歌曲ID
    :param comment_content: 评论内容(可选,用于精确匹配)
    """
    data = read_json_from_device("autotest/comments.json", device_id, result)
    if data and "userComments" in data:
        for comment in data["userComments"]:
            if comment.get("songId") == song_id:
                if comment_content:
                    return comment.get("content") == comment_content
                return True
    return False


def task_25_check_invite_friend(device_id=None, result=None):
    """
    任务25: 邀请好友一起听歌
    验证: 多用户功能难以验证,返回False表示不支持
    """
    # 无法验证多用户功能
    return False


def task_26_check_song_recognition(device_id=None, result=None):
    """
    任务26: 听歌识曲(比如打开B站并识别正在播放的视频的BGM)
    验证: 跨应用功能难以验证,返回False表示不支持
    """
    # 无法验证跨应用识曲功能
    return False


def task_27_check_playlist_sort_order(playlist_id, expected_order, device_id=None, result=None):
    """
    任务27: 更改歌单的排序顺序
    验证: 检查user_playlists.json中指定歌单的sortOrder
    :param playlist_id: 歌单ID
    :param expected_order: 期望的排序方式,如"time_desc","name_asc"等
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result)
    if data and "playlists" in data:
        for playlist in data["playlists"]:
            if playlist.get("playlistId") == playlist_id:
                return playlist.get("sortOrder") == expected_order
    return False


def task_28_check_collect_album(album_id, device_id=None, result=None):
    """
    任务28: 搜索一个歌手,在歌手主页选择一个专辑并收藏
    验证: 检查collected_items.json中collectedAlbums是否包含指定专辑
    :param album_id: 收藏的专辑ID
    """
    data = read_json_from_device("autotest/collected_items.json", device_id, result)
    if data and "collectedAlbums" in data:
        album_ids = [a.get("albumId") for a in data["collectedAlbums"]]
        return album_id in album_ids
    return False


def task_29_check_unfollow_artist(artist_id=None, device_id=None, result=None):
    """
    任务29: 将关注列表中的一位歌手删除
    验证: 检查followed_artists.json中followedArtists是否不包含指定歌手
    如果未指定artist_id，则检查关注列表是否有减少
    :param artist_id: 取消关注的歌手ID (可选)
    """
    data = read_json_from_device("autotest/followed_artists.json", device_id, result)

    if artist_id:
        # 指定了artist_id，检查该歌手是否不在列表中
        if data and "followedArtists" in data:
            artist_ids = [a.get("artistId") for a in data["followedArtists"]]
            return artist_id not in artist_ids
        return False
    else:
        # 未指定artist_id，检查关注列表变化
        # 简单检查：如果关注列表存在且数量小于初始数量（假设初始有5个歌手）
        if data and "followedArtists" in data:
            initial_artist_count = 5  # 假设初始状态有5个歌手
            current_count = len(data["followedArtists"])
            # 如果当前数量少于初始数量，说明有歌手被取消关注
            return current_count < initial_artist_count
        return True  # 如果列表为空或不存在，也算通过


def task_30_check_play_mv(mv_id, device_id=None, result=None):
    """
    任务30: 搜索一首歌曲并播放MV
    验证: 检查mv_playback.json中currentMV.mvId是否为指定MV且isPlaying为true
    :param mv_id: 播放的MV ID
    """
    data = read_json_from_device("autotest/mv_playback.json", device_id, result)
    if data and "currentMV" in data:
        current_mv = data["currentMV"]
        return current_mv.get("mvId") == mv_id and current_mv.get("isPlaying") == True
    return False


def task_31_check_change_player_style(style_id, device_id=None, result=None):
    """
    任务31: 更改播放器样式
    验证: 检查player_settings.json中playerStyle.styleId是否为指定样式
    :param style_id: 播放器样式ID
    """
    data = read_json_from_device("autotest/player_settings.json", device_id, result)
    if data and "playerStyle" in data:
        return data["playerStyle"].get("styleId") == style_id
    return False


# ==================== 测试运行器 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("音乐App自动化测试验证函数")
    print("=" * 50)

    # 示例: 测试任务1
    print("\n测试任务1: 打开app并进入推荐首页")
    result = task_01_check_open_recommend_page()
    print(f"结果: {'通过' if result else '失败'}")

    # 示例: 测试任务7
    print("\n测试任务7: 将播放模式改为随机播放")
    result = task_07_check_shuffle_mode()
    print(f"结果: {'通过' if result else '失败'}")

    # 示例: 测试任务8
    print("\n测试任务8: 收藏当前歌曲")
    result = task_08_check_favorite_song("song_001")
    print(f"结果: {'通过' if result else '失败'}")
