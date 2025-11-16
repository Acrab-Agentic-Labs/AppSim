# -*- coding:utf-8 -*-

from .bilibili import BILIBILI_TASKS
from .gaode import GAODE_TASKS
from .eleme import ELEME_TASKS
from .music import MUSIC_TASKS
from .wechat import WECHAT_TASKS
from .rednote import RED_NOTE_TASKS
from .tencentmeeting import TENCENT_MEETING_TASKS
from .jd import JD_TASKS
from .ctrip import CTRIP_TASKS

from enum import Enum


class AppEnum(Enum):
    BILIBILI = "Bilibili"
    CTRIP = "Ctrip"
    ELEME = "EleMe"
    GAODE = "Gaode"
    MUSIC = "Music"
    MYJD = "MyJD"
    RED_NOTE = "RedNote"
    TENCENT_MEETING = "TencentMeeting"
    WECHAT = "Wechat"


APP_TASKS_MAP = {
    AppEnum.BILIBILI: BILIBILI_TASKS,
    AppEnum.CTRIP: CTRIP_TASKS,
    AppEnum.ELEME: ELEME_TASKS,
    AppEnum.GAODE: GAODE_TASKS,
    AppEnum.MUSIC: MUSIC_TASKS,
    AppEnum.MYJD: JD_TASKS,
    AppEnum.RED_NOTE: RED_NOTE_TASKS,
    AppEnum.TENCENT_MEETING: TENCENT_MEETING_TASKS,
    AppEnum.WECHAT: WECHAT_TASKS,
}
