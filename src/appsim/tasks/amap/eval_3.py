"""
任务：告诉我账号的名字和id。把你的答案放在<ans>和</ans>之间。

答案：
- 名字：高德用户
- id：284834783

步骤：1
"""

import logging
import sys
import re

def validate(result=None, **kwargs):
    """
    宽容模式校验：
    1. 优先从 <ans> 提取，如果没有标签则搜索全文。
    2. 只要全文包含预期的“名字”和“ID”关键字，即视为通过。
    """
    # 预设的两个核心关键信息
    EXPECTED_NAME = "高德用户"
    EXPECTED_ID = "284834783"

    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - AI 未返回任何内容")
        return False

    final_msg = str(result["final_message"])

    # --- 步骤 1: 提取待检测的文本 ---
    # 尝试寻找 <ans> 标签
    tag_match = re.search(r"<ans>\s*(.*?)\s*</ans>", final_msg, re.IGNORECASE | re.DOTALL)
    
    if tag_match:
        # 如果有标签，我们只检测标签里的内容
        text_to_check = tag_match.group(1).strip()
        logging.info(f"  → 从 <ans> 标签中提取到内容: '{text_to_check}'")
    else:
        # 如果没有标签，我们宽容一点，直接检测整个回复全文
        text_to_check = final_msg.strip()
        logging.info("  ⚠ 未找到 <ans> 标签，将对全文进行关键字检索。")

    # --- 步骤 2: 宽容比对 (包含匹配) ---
    # 检查名字和 ID 是否都在提取到的文本中
    # 使用 in 操作符而不是 ==，这样即便 AI 多说了话（如“名字是：xxx”）也能过
    name_found = EXPECTED_NAME in text_to_check
    id_found = EXPECTED_ID in text_to_check

    if name_found and id_found:
        logging.info(f"✓ 检测成功 - 找到了关键信息: '{EXPECTED_NAME}' 和 '{EXPECTED_ID}'")
        return True
    else:
        # 给出详细的错误提示，方便调试
        missing = []
        if not name_found: missing.append(f"名字({EXPECTED_NAME})")
        if not id_found: missing.append(f"ID({EXPECTED_ID})")
        logging.error(f"✗ 检测失败 - 回复中缺少: {', '.join(missing)}")
        return False
if __name__ == "__main__":
    # 配置日志输出格式
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    print("=" * 70)
    print("任务 3：告诉我账号的名字和id")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 点击更多")
    print("  2. 查看名字和id")
    print("\n🔍 正在等待 Runner 调用 AI 进行验证...")

    # --- 模拟测试用例 ---

    # 用例 1：正确且带标签
    test_case_1 = {
        "final_message": "账号名字是 <ans>高德用户</ans>，ID是 <ans>284834783</ans>",
        "expected_eval_result": True,
    }

    # 用例 2：完全无关的回答
    test_case_2 = {
        "final_message": "我无法找到账号信息。",
        "expected_eval_result": False
    }

    # 用例 3：只有名字没有ID（不完整）
    test_case_3 = {
        "final_message": "账号名字是 <ans>高德用户</ans>",
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
