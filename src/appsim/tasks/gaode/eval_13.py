"""
指令 13 验证脚本：告诉我M+购物中心的地址
把你的答案放在 <ans> 和 </ans> 之间。

步骤：3
"""

import logging
import sys
import re


def validate(result=None, **kwargs):
    """
    校验逻辑：
    1. 必须包含完整的地址字符串 "湖北省武汉市江汉区江汉路187号"。
    2. 优先提取 <ans> 标签，若无标签则扫描全文。
    """
    # 这里定义必须出现的【完整】地址内容
    EXPECTED_FULL_ADDRESS = "湖北省武汉市江汉区江汉路187号"

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

    # 3. 严格比对逻辑：必须包含完整的地址信息
    # 如果文本中只说了 "江汉路187号"，则完整地址匹配会失败
    if EXPECTED_FULL_ADDRESS in text_to_check:
        logging.info(f"✓ 检测成功 - 匹配到完整地址: '{EXPECTED_FULL_ADDRESS}'")
        return True
    else:
        logging.error(f"✗ 检测失败 - 未能匹配到完整地址。")
        logging.error(f"  期望: '{EXPECTED_FULL_ADDRESS}'")
        return False


if __name__ == "__main__":
    # 配置日志输出格式
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    print("=" * 70)
    print("任务 13 逻辑验证：M+购物中心地址 (严格匹配模式)")
    print("=" * 70)
    print("\n🔍 正在进行模拟 Case 验证...")

    # --- 模拟测试用例 ---
    
    # 用例 1：正确且带标签
    test_case_1 = {
        "final_message": "M+购物中心的地址是 <ans>湖北省武汉市江汉区江汉路187号</ans>",
        "expected_eval_result": True,
    }
    
    # 用例 2：回答不相关
    test_case_2 = {
        "final_message": "我无法查询到该购物中心的具体地址。", 
        "expected_eval_result": False
    }
    
    # 用例 3：地址不完整（缺少省市区，只说了街道和门牌号）
    test_case_3 = {
        "final_message": "地址是 <ans>江汉路187号</ans>",
        "expected_eval_result": False # 根据要求，不完整输出算错误
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
    print(f"任务 13 模拟测试完成：通过 {total_passed}/{len(all_tests)}")
    print("=" * 70)
    
    # 如果模拟测试全部通过，则退出码为0
    sys.exit(0 if total_passed == len(all_tests) else 1)