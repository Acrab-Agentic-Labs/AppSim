#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计模型在不同难度级别和推理任务上的准确率
"""

import os
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from enum import Enum


from appsim.tasks.base import TaskItem, AppTasks
from appsim.tasks import AppEnum, APP_TASKS_MAP


def load_results_from_jsonl(jsonl_file_path):
    """从.jsonl文件中加载结果，使用 instruction 作为 key"""
    import re
    results = {}

    try:
        with open(jsonl_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                instruction = None
                verify_result = False

                try:
                    # 尝试完整解析JSON
                    data = json.loads(line)
                    instruction = data.get('instruction')
                    verify_result_raw = data.get('verify_result', False)
                    # 只有当 verify_result 是布尔值 True 时才算成功
                    verify_result = verify_result_raw is True

                except json.JSONDecodeError:
                    # JSON解析失败，使用正则表达式提取关键字段
                    # 提取 "instruction": "..."
                    instruction_match = re.search(r'"instruction"\s*:\s*"([^"]*)"', line)
                    if instruction_match:
                        instruction = instruction_match.group(1)

                    # 提取 "verify_result": 值，检查是否为布尔值 true (不是字符串 "true")
                    # 使用负向前瞻确保 true 前面没有引号
                    verify_match = re.search(r'"verify_result"\s*:\s*(?!")true(?=\s*[,}\]])', line)
                    verify_result = verify_match is not None

                    if instruction is not None:
                        print(f"警告: 第 {line_num} 行 JSON 解析失败，使用正则提取 (instruction={instruction[:50]}..., verify_result={verify_result})")

                if instruction is not None:
                    results[instruction] = verify_result

    except Exception as e:
        print(f"警告: 加载 {jsonl_file_path} 时出错: {e}")

    return results


def get_difficulty_level(human_steps):
    """根据human_steps确定难度等级"""
    if 0 <= human_steps <= 5:
        return 'L1'
    elif 6 <= human_steps <= 10:
        return 'L2'
    else:
        return 'L3'


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='统计模型在不同难度级别和推理任务上的准确率')
    parser.add_argument('--results_dir', type=str, required=True, help='结果文件目录路径')
    args = parser.parse_args()
    
    # 定义路径
    base_dir = Path(__file__).parent
    results_dir = base_dir / args.results_dir

    # 统计数据
    difficulty_stats = {
        'L1': {'correct': 0, 'total': 0},
        'L2': {'correct': 0, 'total': 0},
        'L3': {'correct': 0, 'total': 0}
    }

    reasoning_stats = {
        'correct': 0,
        'total': 0
    }

    non_reasoning_stats = {
        'correct': 0,
        'total': 0
    }

    overall_stats = {
        'correct': 0,
        'total': 0
    }

    # 详细统计（按应用）
    app_details = defaultdict(lambda: {
        'L1': {'correct': 0, 'total': 0},
        'L2': {'correct': 0, 'total': 0},
        'L3': {'correct': 0, 'total': 0},
        'reasoning': {'correct': 0, 'total': 0},
        'non_reasoning': {'correct': 0, 'total': 0},
        'overall': {'correct': 0, 'total': 0}
    })

    # 遍历所有应用
    for app_enum, tasks in APP_TASKS_MAP.items():
        if not tasks or not tasks.task_items:
            print(f"警告: {app_enum.value} 没有加载到任务")
            continue

        # 查找对应的结果文件（使用应用名称作为前缀）
        app_name = app_enum.value
        result_file = None
        for file in results_dir.glob(f'eval_details_{app_name}*.jsonl'):
            result_file = file
            break

        if not result_file:
            continue

        # 加载结果
        results = load_results_from_jsonl(str(result_file))

        print(f"\n处理应用: {app_enum.value}")
        print(f"  结果文件: {result_file.name}")
        print(f"  任务数量: {len(tasks.task_items)}")
        print(f"  结果数量: {len(results)}")
        
        assert len(results) == len(tasks.task_items), f"结果数量: {len(results)} 任务数量: {len(tasks.task_items)} 不一致"

        # 统计每个任务
        for task in tasks.task_items:
            instruction = task.instruction
            human_steps = task.human_steps
            is_reasoning = task.is_reasoning

            # 获取验证结果（根据 instruction 匹配）
            if instruction not in results:
                print(f"  警告: 任务 '{instruction[:50]}...' 没有结果")
                continue

            verify_result = results[instruction]
            difficulty = get_difficulty_level(human_steps)

            # 更新整体统计
            overall_stats['total'] += 1
            if verify_result:
                overall_stats['correct'] += 1

            # 更新难度统计
            difficulty_stats[difficulty]['total'] += 1
            if verify_result:
                difficulty_stats[difficulty]['correct'] += 1

            # 更新推理任务统计
            if is_reasoning:
                reasoning_stats['total'] += 1
                if verify_result:
                    reasoning_stats['correct'] += 1
            else:
                non_reasoning_stats['total'] += 1
                if verify_result:
                    non_reasoning_stats['correct'] += 1

            # 更新应用级别的详细统计
            app_name = app_enum.value
            app_details[app_name]['overall']['total'] += 1
            if verify_result:
                app_details[app_name]['overall']['correct'] += 1

            app_details[app_name][difficulty]['total'] += 1
            if verify_result:
                app_details[app_name][difficulty]['correct'] += 1

            if is_reasoning:
                app_details[app_name]['reasoning']['total'] += 1
                if verify_result:
                    app_details[app_name]['reasoning']['correct'] += 1
            else:
                app_details[app_name]['non_reasoning']['total'] += 1
                if verify_result:
                    app_details[app_name]['non_reasoning']['correct'] += 1

    if overall_stats['total'] == 0:
        print("\n无统计数据")
        return

    # 保存结果到文件（使用结果目录名作为输出文件名，改为 .md 格式）
    results_dir_name = results_dir.name
    output_file = base_dir / f'{results_dir_name}_accuracy_report.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 准确率统计报告\n\n")
        f.write("## 整体统计\n\n")

        # 整体准确率表格
        f.write("| 指标 | 正确数 | 总数 | 准确率 |\n")
        f.write("|------|--------|------|--------|\n")
        overall_acc = overall_stats['correct']/overall_stats['total']*100 if overall_stats['total'] > 0 else 0
        f.write(f"| 总体准确率 | {overall_stats['correct']} | {overall_stats['total']} | {overall_acc:.2f}% |\n\n")

        # 按难度级别统计表格
        f.write("## 按难度级别统计\n\n")
        f.write("| 难度级别 | Steps 范围 | 正确数 | 总数 | 准确率 |\n")
        f.write("|---------|-----------|--------|------|--------|\n")
        for level in ['L1', 'L2', 'L3']:
            stats = difficulty_stats[level]
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total'] * 100
                steps_range = '0-5' if level=='L1' else '6-10' if level=='L2' else '11+'
                f.write(f"| {level} | {steps_range} | {stats['correct']} | {stats['total']} | {accuracy:.2f}% |\n")
        f.write("\n")

        # 按任务类型统计表格
        f.write("## 按任务类型统计\n\n")
        f.write("| 任务类型 | 正确数 | 总数 | 准确率 |\n")
        f.write("|---------|--------|------|--------|\n")
        if reasoning_stats['total'] > 0:
            reasoning_accuracy = reasoning_stats['correct'] / reasoning_stats['total'] * 100
            f.write(f"| 推理任务 (Reasoning) | {reasoning_stats['correct']} | {reasoning_stats['total']} | {reasoning_accuracy:.2f}% |\n")
        if non_reasoning_stats['total'] > 0:
            non_reasoning_accuracy = non_reasoning_stats['correct'] / non_reasoning_stats['total'] * 100
            f.write(f"| 非推理任务 (Non-reasoning) | {non_reasoning_stats['correct']} | {non_reasoning_stats['total']} | {non_reasoning_accuracy:.2f}% |\n")
        f.write("\n")

        # 各应用详细统计表格
        f.write("## 各应用详细统计\n\n")
        f.write("| 应用 | L1 | L2 | L3 | Reasoning | Non-reasoning | 总体 |\n")
        f.write("|------|----|----|----|-----------|--------------:|------|\n")

        for app_name in sorted(app_details.keys()):
            stats = app_details[app_name]

            # 计算各项准确率
            l1_acc = f"{stats['L1']['correct']}/{stats['L1']['total']}" if stats['L1']['total'] > 0 else "-"
            l2_acc = f"{stats['L2']['correct']}/{stats['L2']['total']}" if stats['L2']['total'] > 0 else "-"
            l3_acc = f"{stats['L3']['correct']}/{stats['L3']['total']}" if stats['L3']['total'] > 0 else "-"
            reasoning_acc = f"{stats['reasoning']['correct']}/{stats['reasoning']['total']}" if stats['reasoning']['total'] > 0 else "-"
            non_reasoning_acc = f"{stats['non_reasoning']['correct']}/{stats['non_reasoning']['total']}" if stats['non_reasoning']['total'] > 0 else "-"
            overall_acc = f"{stats['overall']['correct']}/{stats['overall']['total']}" if stats['overall']['total'] > 0 else "-"

            f.write(f"| {app_name} | {l1_acc} | {l2_acc} | {l3_acc} | {reasoning_acc} | {non_reasoning_acc} | {overall_acc} |\n")

        f.write("\n")

        # 添加详细的应用统计（含百分比）
        f.write("## 各应用详细统计（含准确率）\n\n")
        for app_name in sorted(app_details.keys()):
            stats = app_details[app_name]
            f.write(f"### {app_name}\n\n")
            f.write("| 类别 | 正确数 | 总数 | 准确率 |\n")
            f.write("|------|--------|------|--------|\n")

            overall = stats['overall']
            if overall['total'] > 0:
                f.write(f"| 总体 | {overall['correct']} | {overall['total']} | {overall['correct']/overall['total']*100:.2f}% |\n")

            for level in ['L1', 'L2', 'L3']:
                level_stats = stats[level]
                if level_stats['total'] > 0:
                    acc = level_stats['correct'] / level_stats['total'] * 100
                    f.write(f"| {level} | {level_stats['correct']} | {level_stats['total']} | {acc:.2f}% |\n")

            reasoning = stats['reasoning']
            if reasoning['total'] > 0:
                f.write(f"| 推理任务 | {reasoning['correct']} | {reasoning['total']} | {reasoning['correct']/reasoning['total']*100:.2f}% |\n")

            non_reasoning = stats['non_reasoning']
            if non_reasoning['total'] > 0:
                f.write(f"| 非推理任务 | {non_reasoning['correct']} | {non_reasoning['total']} | {non_reasoning['correct']/non_reasoning['total']*100:.2f}% |\n")

            f.write("\n")

    # 使用 rich 库打印 output_file 中的内容
    from rich.console import Console
    from rich.markdown import Markdown
    
    console = Console()
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    console.print(Markdown(content))


if __name__ == '__main__':
    main()
