"""
检测脚本 #17: 给首页第一条帖子设置"不感兴趣"
难度: 2 (中等)
检测方式: 检查菜单操作后是否已关闭（Not interested已被选择）
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 操作完成后，菜单应该已消失
    menu_visible = ui.has_text("Not interested") and ui.has_text("Report")

    if menu_visible:
        # 菜单仍然可见，可能还没点击Not interested
        return result_fail("菜单仍然可见，'不感兴趣'可能未被选择")

    # 检查 snackbar/toast 提示 "Not interested" (菜单已消失但反馈仍在)
    if ui.has_text("Not interested"):
        return result_pass("检测到Not interested反馈")

    # 菜单已消失且回到首页 — 可能操作成功也可能只是按了返回
    if ui.has_text("Instagram"):
        # 检查帖子是否被移除（feed 内容变化）
        if ui.has_text("Undo"):
            return result_pass("已成功设置'不感兴趣'（检测到Undo提示）")
        return result_fail("已返回首页但无法确认'不感兴趣'是否生效")

    return result_fail("未检测到'不感兴趣'操作结果")


if __name__ == "__main__":
    run_check(check)
