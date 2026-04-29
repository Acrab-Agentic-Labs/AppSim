"""
指令 11 验证脚本：告诉我步行去最近的酒店需要几分钟 把你的答案放在<ans>和</ans>之间。

答案：8分钟 或 8 或 八分钟

步骤：5
"""
import logging
import sys
import re

def validate(result=None, **kwargs):
    """
    更宽容的校验器：
    只要 AI 的回答中包含了关键词列表里的【任意一个】，就算通过。
    """
    # 这里放所有可能的正确表达方式（比如数字和汉字大写）
    EXPECTED_KEYWORDS = ["8", "八","8分钟","八分钟"] 

    if not result or "final_message" not in result:
        return False

    final_msg = str(result["final_message"])

    # 1. 提取检测范围（有标签看标签，没标签看全文）
    tag_match = re.search(r"<ans>\s*(.*?)\s*</ans>", final_msg, re.IGNORECASE | re.DOTALL)
    text_to_check = tag_match.group(1).strip() if tag_match else final_msg.strip()

    # 2. 宽容匹配逻辑：使用 any()
    # 只要 EXPECTED_KEYWORDS 里的【任意一个】词在 text_to_check 中，就返回 True
    is_correct = any(kw in text_to_check for kw in EXPECTED_KEYWORDS)

    if is_correct:
        logging.info(f"✅ 检测成功！匹配到关键信息之一: {EXPECTED_KEYWORDS}")
        return True
    else:
        logging.error(f"❌ 检测失败！回复中未匹配到预设关键词。预期其中之一: {EXPECTED_KEYWORDS}, 实际得到: '{text_to_check}'")
        return False

if __name__ == "__main__":
    # 配置日志输出格式
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    print("=" * 70)
    print("任务 11：告诉我步行去最近的酒店需要几分钟")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 点击周边")
    print("  2. 点击酒店并且搜索当前位置周边")
    print("\n🔍 正在等待 Runner 调用 AI 进行验证...")

    # --- 模拟测试用例 ---

    # 用例 1：正确且带标签
    test_case_1 = {
        "final_message": "步行去最近的酒店需要 <ans>8分钟</ans>",
        "expected_eval_result": True,
    }

    # 用例 2：完全无关的回答
    test_case_2 = {
        "final_message": "我无法找到附近的酒店信息。",
        "expected_eval_result": False
    }

    # 用例 3：错误的时间
    test_case_3 = {
        "final_message": "步行去最近的酒店需要 <ans>15分钟</ans>",
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