# -*- coding:utf-8 -*-

from enum import Enum

from .bilibili import BILIBILI_TASKS
from .ctrip import CTRIP_TASKS
from .eleme import ELEME_TASKS
from .gaode import GAODE_TASKS
from .jd import JD_TASKS
from .music import MUSIC_TASKS
from .rednote import RED_NOTE_TASKS
from .tencentmeeting import TENCENT_MEETING_TASKS
from .ubereats import UBEREATS_TASKS
from .wechat import WECHAT_TASKS
from .youtube import YOUTUBE_TASKS
from .amazon import AMAZON_TASKS
from .whatsapp import WHATSAPP_TASKS
from .zoom import ZOOM_TASKS
from .booking import BOOKING_TASKS
from .spotify import SPOTIFY_TASKS
from .instagram import INSTAGRAM_TASKS

class AppEnum(Enum):
    BILIBILI = "Bilibili"
    CTRIP = "ctrip_sim"
    ELEME = "EleMe"
    GAODE = "Gaode"
    MUSIC = "Music"
    MYJD = "MyJD"
    RED_NOTE = "RedNote"
    TENCENT_MEETING = "TencentMeeting"
    UBEREATS = "UberEats"
    WECHAT = "Wechat"
    YOUTUBE = "YouTube"
    AMAZON = "Amazon"
    WHATSAPP = "WhatsApp"
    BOOKING = "Booking"
    ZOOM = "Zoom"
    SPOTIFY = "Spotify"
    INSTAGRAM = "Instagram"

APP_TASKS_MAP = {
    AppEnum.BILIBILI: BILIBILI_TASKS,
    AppEnum.CTRIP: CTRIP_TASKS,
    AppEnum.ELEME: ELEME_TASKS,
    AppEnum.GAODE: GAODE_TASKS,
    AppEnum.MUSIC: MUSIC_TASKS,
    AppEnum.MYJD: JD_TASKS,
    AppEnum.RED_NOTE: RED_NOTE_TASKS,
    AppEnum.TENCENT_MEETING: TENCENT_MEETING_TASKS,
    AppEnum.UBEREATS: UBEREATS_TASKS,
    AppEnum.WECHAT: WECHAT_TASKS,
    AppEnum.YOUTUBE: YOUTUBE_TASKS,
    AppEnum.AMAZON: AMAZON_TASKS,
    AppEnum.WHATSAPP: WHATSAPP_TASKS,
    AppEnum.ZOOM: ZOOM_TASKS,
    AppEnum.BOOKING: BOOKING_TASKS,
    AppEnum.SPOTIFY: SPOTIFY_TASKS,
    AppEnum.INSTAGRAM: INSTAGRAM_TASKS,
}
