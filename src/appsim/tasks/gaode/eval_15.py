"""
指令 15 验证脚本：告诉我收藏的第一个饭店的名称
把你的答案放在 <ans> 和 </ans> 之间。

步骤：2
"""

import logging
import sys
import re


def validate(result=None, **kwargs):
    """
    校验逻辑：
    1. 必须包含完整的饭店名称 "肖记公安牛肉鱼杂馆"。
    2. 优先提取 <ans> 标签，若无标签则扫描全文。
    """
    # 这里定义必须出现的【完整】饭店名称
    EXPECTED_FULL_NAME = "肖记公安牛肉鱼杂馆"

    # 1. 检查结果是否存在
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - AI 未能生成任何回复。")
        return False

    final_msg = str(result["final_message"])

    # 2. 提取待检测文本 (优先正则匹配 <ans>内容 </ans>)
    tag_match = re.search(
        r"<ans>\s*(.*?)\s*</ans>", final_msg, re.IGNORECASE | re.DOTALL
    )

    if tag_match:
        text_to_check = tag_match.group(1).strip()
        logging.info(f"  → 标签提取内容: '{text_to_check}'")
    else:
        # 宽容处理：如果没有标签，检查全文
        text_to_check = final_msg.strip()
        logging.warning("  ⚠ 未找到标签，正在检索全文...")

    # 3. 严格比对逻辑：必须包含完整的店名
    # 如果文本中只说了 "公安牛肉鱼杂馆"，则全名匹配会失败
    if EXPECTED_FULL_NAME in text_to_check:
        logging.info(f"✓ 检测成功 - 匹配到完整店名: '{EXPECTED_FULL_NAME}'")
        return True
    else:
        logging.error(f"✗ 检测失败 - 未能匹配到完整店名。")
        logging.error(f"  期望: '{EXPECTED_FULL_NAME}'")
        return False


if __name__ == "__main__":
    # 配置日志输出格式
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    print("=" * 70)
    print("任务 15 逻辑验证：收藏夹第一行饭店名称 (严格匹配模式)")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入‘收藏’或‘我的收藏’页面")
    print("  2. 查看‘地点’分类下收藏的第一行项目内容")
    print("  3. 确认名称为 肖记公安牛肉鱼杂馆")
    print("\n🔍 正在进行模拟 Case 验证...")

    # --- 模拟测试用例 ---
    
    # 用例 1：正确且带标签
    test_case_1 = {
        "final_message": "你收藏的第一行饭店是 <ans>肖记公安牛肉鱼杂馆</ans>",
        "expected_eval_result": True,
    }
    
    # 用例 2：回答找不到或内容错误
    test_case_2 = {
        "final_message": "你的收藏夹里没有任何饭店信息。", 
        "expected_eval_result": False
    }
    
    # 用例 3：名称不完整（缺少前缀“肖记”）
    test_case_3 = {
        "final_message": "第一行是 <ans>公安牛肉鱼杂馆</ans>",
        "expected_eval_result": False # 缺少前缀，判定为不完整/错误
    }

    # 开始执行模拟测试
    all_tests = [test_case_1, test_case_2, test_case_3]
    total_passed = 0

    for idx, test in enumerate(all_tests, 1):
        logging.info(f"\n[测试用例 {idx}]")
        actual_result = validate(result=test)
        expected_result = test["expected_eval_result"]
        
        if actual_result == expected_result:
            logging.info(f"✅ 结果符合预期 (实际: {actual_result})")
            total_passed += 1
        else:
            logging.error(f"❌ 结果不符合预期！实际: {actual_result}, 期望: {expected_result}")

    print("\n" + "=" * 70)
    print(f"任务 15 模拟测试完成：通过 {total_passed}/{len(all_tests)}")
    print("=" * 70)
    
    # 如果模拟测试全部通过，则退出码为0
    sys.exit(0 if total_passed == len(all_tests) else 1)