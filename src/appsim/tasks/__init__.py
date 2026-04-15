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
from .zoom import ZOOM_TASKS
from .booking import BOOKING_TASKS
from .wechat import WECHAT_TASKS


class AppEnum(Enum):
    BILIBILI = "Bilibili"
    BOOKING = "Booking"
    CTRIP = "Ctrip"
    ELEME = "EleMe"
    GAODE = "Gaode"
    MUSIC = "Music"
    MYJD = "MyJD"
    RED_NOTE = "RedNote"
    TENCENT_MEETING = "TencentMeeting"
    ZOOM = "Zoom"
    WECHAT = "Wechat"


APP_TASKS_MAP = {
    AppEnum.BILIBILI: BILIBILI_TASKS,
    AppEnum.BOOKING: BOOKING_TASKS,
    AppEnum.CTRIP: CTRIP_TASKS,
    AppEnum.ELEME: ELEME_TASKS,
    AppEnum.GAODE: GAODE_TASKS,
    AppEnum.MUSIC: MUSIC_TASKS,
    AppEnum.MYJD: JD_TASKS,
    AppEnum.RED_NOTE: RED_NOTE_TASKS,
    AppEnum.TENCENT_MEETING: TENCENT_MEETING_TASKS,
    AppEnum.ZOOM: ZOOM_TASKS,
    AppEnum.WECHAT: WECHAT_TASKS,
}
