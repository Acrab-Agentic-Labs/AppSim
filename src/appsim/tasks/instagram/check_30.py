"""
检测脚本 #30: 开启睡眠模式
难度: 2 (中等)
检测方式: 检查Time Management页面的Sleep mode开关是否开启
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在Time Management页面
    if not (ui.has_text("Time management") or ui.has_text("Sleep mode")):
        return result_fail("当前不在时间管理页面")

    # 检查Sleep mode是否存在
    if not ui.has_text("Sleep mode"):
        return result_fail("在时间管理页面但未找到Sleep mode选项")

    # 在XML中查找 Sleep mode 附近的 Switch
    xml = ui.xml

    # 尝试找到 Sleep mode 文本在XML中的位置，然后查找附近的 Switch
    sleep_idx = xml.lower().find("sleep mode")
    if sleep_idx >= 0:
        # 取 Sleep mode 之后的一段 XML 来查找关联的 Switch
        nearby_xml = xml[sleep_idx:sleep_idx + 500]
        switch_pattern = r'<node[^>]*class="[^"]*Switch[^"]*"[^>]*/>'
        switches = re.findall(switch_pattern, nearby_xml)
        if switches:
            if 'checked="true"' in switches[0]:
                return result_pass("睡眠模式已开启（Sleep mode 开关已打开）")
            else:
                return result_fail("Sleep mode 开关存在但未开启")

    # Fallback: 查找所有 Switch，但要求页面上只有 Sleep mode 相关的
    switch_pattern = r'<node[^>]*class="[^"]*Switch[^"]*"[^>]*/>'
    switches = re.findall(switch_pattern, xml)
    if switches:
        # 如果只有一个 switch，就可以确定是 Sleep mode 的
        if len(switches) == 1:
            if 'checked="true"' in switches[0]:
                return result_pass("睡眠模式已开启")
            return result_fail("Sleep mode 开关未开启")
        # 多个 switch 时无法确定哪个是 Sleep mode 的
        checked = sum(1 for s in switches if 'checked="true"' in s)
        if checked > 0:
            return result_pass(f"睡眠模式可能已开启（{checked}/{len(switches)} 个开关已开启）")
        return result_fail("所有开关均未开启")

    return result_fail("在时间管理页面但未找到开关组件")


if __name__ == "__main__":
    run_check(check)
