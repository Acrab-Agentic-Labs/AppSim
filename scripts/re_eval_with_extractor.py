"""
临时脚本：使用新的 answer_schema 提取方案重新评测已有结果。

用法:
  python re_eval_with_extractor.py <result_jsonl_path> --task WECHAT

会读取原始 JSONL 结果，对 answer 类任务用 BaselineExtractor 重新提取并验证，
输出对比结果到同目录下 re_eval_*.jsonl。
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from appsim.answer_extractor import BaselineExtractor
from appsim.tasks import APP_TASKS_MAP, AppEnum


def parse_args():
    parser = argparse.ArgumentParser(description="用新 schema 方案重新评测已有结果")
    parser.add_argument("result_file", type=str, help="原始结果 JSONL 文件路径")
    parser.add_argument(
        "--task", "-t", type=str, required=True,
        choices=[app.name for app in AppEnum],
        help="对应的 App 任务名",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="输出文件路径（默认: 同目录下 re_eval_<原文件名>）",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    task_app = AppEnum[args.task]
    tasks = APP_TASKS_MAP[task_app]
    task_items = tasks.task_items

    extractor = BaselineExtractor()

    # 读取原始结果
    with open(args.result_file, "r", encoding="utf-8") as f:
        results = [json.loads(line) for line in f if line.strip()]

    # 输出路径
    if args.output:
        output_path = args.output
    else:
        dirname = os.path.dirname(args.result_file)
        basename = os.path.basename(args.result_file)
        output_path = os.path.join(dirname, f"re_eval_{basename}")

    print(f"原始结果: {args.result_file} ({len(results)} 条)")
    print(f"输出路径: {output_path}")
    print(f"任务定义: {task_app.name} ({len(task_items)} 个任务)")
    print("-" * 60)

    changed = 0
    total_answer = 0

    with open(output_path, "w", encoding="utf-8") as out_f:
        for item_detail in results:
            task_id = item_detail["id"]
            if task_id >= len(task_items):
                print(f"[SKIP] id={task_id} 超出任务定义范围")
                out_f.write(json.dumps(item_detail, ensure_ascii=False) + "\n")
                continue

            task_item = task_items[task_id]
            result_payload = item_detail["result"]
            old_verify = item_detail["verify_result"]

            # 只处理 answer/hybrid 类型且有 schema 的任务
            if task_item.evaluation_type not in ("answer", "hybrid") or not task_item.answer_schema:
                out_f.write(json.dumps(item_detail, ensure_ascii=False) + "\n")
                continue

            total_answer += 1
            final_message = result_payload.get("final_message")

            # 用 extractor 提取答案
            extraction = extractor.extract(
                final_message=final_message,
                answer_schema=task_item.answer_schema,
                instruction=task_item.instruction,
            )
            result_payload["extracted_answer"] = extraction.answer
            result_payload["no_canonicalize_answer"] = extraction.no_canonicalize_answer
            result_payload["answer_extraction"] = extraction.model_dump()

            # 重新验证
            try:
                new_verify = task_item.verify_func(
                    result=result_payload, device_id=None, backup_dir=None
                )
            except Exception as e:
                new_verify = f"验证异常: {e}"

            item_detail["result"] = result_payload
            item_detail["old_verify_result"] = old_verify
            item_detail["verify_result"] = new_verify
            item_detail["evaluation_type"] = task_item.evaluation_type

            status = ""
            if old_verify != new_verify:
                changed += 1
                status = " [CHANGED]"
            print(
                f"[{task_id:>2}] {task_item.instruction[:30]}... "
                f"old={old_verify} -> new={new_verify}{status}"
            )
            print(f"     final_message: {repr(final_message)[:80]}")
            print(f"     extracted: {extraction.answer}")
            if extraction.error:
                print(f"     ERROR: {extraction.error}")

            out_f.write(json.dumps(item_detail, ensure_ascii=False) + "\n")

    print("-" * 60)
    print(f"answer 类任务: {total_answer}, 结果变化: {changed}")
    print(f"结果已保存到: {output_path}")


if __name__ == "__main__":
    main()
