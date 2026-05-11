"""
指令 23 验证脚本：告诉我江汉大学（汉口校区）周边美食排行榜第一名是什么，把你的答案放在 <ans> 和 </ans> 之间。

答案：Smile and Salad

步骤：6
"""

import logging
import sys
import re

def validate(result=None, **kwargs):
    """
    宽容模式校验器：
    1. 优先提取 <ans> 标签内容，若无标签则扫描全文。
    2. 只要回答中包含预设的关键字（之一）即可通过，不要求完全匹配。
    """
    # 【宽容设置】这里定义正确答案的关键字列表
    # 只要 AI 提到了其中任何一个词，就算对
    EXPECTED_KEYWORDS = ["Smile and Salad"]

    # 1. 检查结果是否存在
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - AI 未能生成任何回复。")
        return False

    final_msg = str(result["final_message"])

    # 2. 提取待检测文本 (正则匹配 <ans>内容 </ans>)
    tag_match = re.search(r"<ans>\s*(.*?)\s*</ans>", final_msg, re.IGNORECASE | re.DOTALL)
    
    if tag_match:
        text_to_check = tag_match.group(1).strip()
        logging.info(f"  → 从 <ans> 标签中提取到: '{text_to_check}'")
    else:
        # 宽容处理：如果没有标签，直接搜索全文
        text_to_check = final_msg.strip()
        logging.warning("  ⚠ 未找到 <ans> 标签，已转为全文模糊匹配。")

    # 3. 宽容比对逻辑：any() 只要匹配到一个关键字就通过
    is_correct = any(kw in text_to_check for kw in EXPECTED_KEYWORDS)

    if is_correct:
        logging.info(f"✓ 检测成功 - AI 回复包含了正确关键字: {EXPECTED_KEYWORDS}")
        return True
    else:
        logging.error(f"✗ 检测失败 - 回复中未找到正确答案。")
        logging.error(f"  期望包含: {EXPECTED_KEYWORDS}")
        logging.error(f"  实际提取内容: '{text_to_check}'")
        return False

if __name__ == "__main__":
    # 配置日志输出格式
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    print("=" * 70)
    print("任务 23：告诉我江汉大学（汉口校区）周边美食排行榜第一名是什么")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 搜索江汉大学（汉口校区）")
    print("  2. 查看周边美食排行榜")
    print("\n🔍 正在等待 Runner 调用 AI 进行验证...")

    # --- 模拟测试用例 ---

    # 用例 1：正确且带标签
    test_case_1 = {
        "final_message": "江汉大学（汉口校区）周边美食排行榜第一名是 <ans>Smile and Salad</ans>",
        "expected_eval_result": True,
    }

    # 用例 2：完全无关的回答
    test_case_2 = {
        "final_message": "我无法找到该校区周边的美食排行榜信息。",
        "expected_eval_result": False
    }

    # 用例 3：错误的店名
    test_case_3 = {
        "final_message": "江汉大学（汉口校区）周边美食排行榜第一名是 <ans>Smile</ans>",
        "expected_eval_result": False
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
    print(f"模拟测试完成：通过 {total_passed}/{len(all_tests)}")
    print("=" * 70)

    # 如果模拟测试全部通过，则退出码为0
    sys.exit(0 if total_passed == len(all_tests) else 1)
