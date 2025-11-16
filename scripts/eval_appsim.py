import logging
from math import log
import os
import sys
import time
import argparse
import json
from tqdm import tqdm


from appsim.utils import run_app_with_clear_data
from appsim.tasks import AppEnum, APP_TASKS_MAP

from dotenv import load_dotenv

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from agent_factory import AgentEnum, create_agent
except ImportError:
    raise ImportError("agent_factory.py 文件不存在")

load_dotenv(override=True, verbose=True)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="评估 M3A Agent 在指定应用上的表现",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例用法:
  在环境变量或者.env文件中配置 OPENAI_API_KEY 和 OPENAI_API_BASE (可选)

  python eval_m3a_agent.py --task BILIBILI --device-id emulator-5554
  python eval_m3a_agent.py -t WECHAT -d emulator-5554
  python eval_m3a_agent.py -t GAODE -d emulator-5554 --output-dir results --agent-name gpt-4o

可用的任务选项: {", ".join([app.name for app in AppEnum])}
        """,
    )

    parser.add_argument(
        "--agent-name",
        type=str,
        required=True,
        choices=[agent.value for agent in AgentEnum],
        help="Agent 名称 (默认: Seed-1.5-VL)",
    )

    parser.add_argument(
        "--task",
        "-t",
        type=str,
        required=True,
        choices=[app.name for app in AppEnum],
        help="要评估的应用任务 (默认: BILIBILI)",
    )

    parser.add_argument("--device-id", "-d", type=str, required=True, help="设备ID")

    parser.add_argument("--output-dir", type=str, default="./output/", help="结果输出目录 (默认: ./output/)")

    parser.add_argument("--start-index", type=int, default=0, help="任务开始的索引")

    parser.add_argument("--end-index", type=int, default=None, help="任务结束的索引（默认: 任务总数）")

    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # 解析任务
    try:
        task_app = AppEnum[args.task]
    except KeyError:
        logging.error(f"❌ 错误: 无效的任务名称 '{args.task}'")
        logging.error(f"可用的任务: {', '.join([app.name for app in AppEnum])}")
        sys.exit(1)

    agent_name = AgentEnum(args.agent_name)
    tasks = APP_TASKS_MAP[task_app]
    device_id = args.device_id
    app_package = tasks.package_name
    start_task_index = args.start_index
    end_task_index = args.end_index if args.end_index is not None else len(tasks.task_items)
    if end_task_index > len(tasks.task_items):
        logging.error(f"❌ 错误: 结束索引超出任务总数 {len(tasks.task_items)}")
        sys.exit(1)

    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)

    # 设置截图目录为 output-dir/screenshots/{package_name}
    screenshots_dir = os.path.join(args.output_dir, "screenshots", app_package)
    os.makedirs(screenshots_dir, exist_ok=True)

    # 构造 Agent
    try:
        agent = create_agent(agent_name, device_id, screenshots_dir)
        logging.info("✅ M3A Agent 初始化成功！")
        logging.info(f"   任务: {task_app.name}")
        logging.info(f"   设备ID: {device_id}")
        logging.info(f"   模型: {agent_name}")
        logging.info(f"   输出目录: {args.output_dir}")
        logging.info(f"   截图目录: {screenshots_dir}")
    except Exception as e:
        logging.error(f"❌ 初始化失败: {e}")
        raise e

    # 创建输出文件路径（含时间戳）
    output_filename = f"eval_details_{task_app.value}_{time.strftime('%Y%m%d_%H%M%S')}.jsonl"
    output_path = os.path.join(args.output_dir, output_filename)
    logging.info(f"结果将实时保存到: {output_path}")

    # 开始执行任务
    for id, item in enumerate(tasks.task_items[start_task_index:end_task_index], start=start_task_index):
        # 先初始化设备：重启机器(保证其在首页)+清理app数据（防止干扰）
        instruction = item.instruction
        verify_function = item.verify_func

        # 重置 App 和 Emulator 状态
        run_app_with_clear_data(app_package=app_package, device_id=device_id)

        ItemEvalDetail = {
            "id": id,
            "instruction": instruction,
            "result": None,  # 执行结果
            "verify_result": None,  # 检验结果
        }

        # 重置 Agent （历史对话记录清空）
        agent.reset()

        # 执行指令
        result = agent.execute_instruction(instruction)
        ItemEvalDetail["result"] = result.model_dump()

        if result.success:
            logging.info("✅ 指令执行成功！")
            try:
                verify_result = verify_function(device_id=device_id, result=result.model_dump())
            except Exception as e:
                logging.error(e)
                logging.error(result)
                verify_result = "验证失败（验证函数可能有问题）"

            logging.info(f"{id + 1}/{len(tasks.task_items)}. {instruction} -> 验证结果: {verify_result}")
            ItemEvalDetail["verify_result"] = verify_result
        else:
            logging.error(f"{id + 1}/{len(tasks.task_items)}. {instruction} -> 指令执行失败")

        # 每次循环立即写入一行结果
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(ItemEvalDetail, ensure_ascii=False) + "\n")

    # 关闭 Agent
    try:
        agent.close()
    except Exception as e:
        logging.error(f"关闭 Agent 时出错: {e}")

    # 任务执行完毕
    logging.info("=====================任务执行完毕=============================")
    logging.info(f"所有结果已保存到: {output_path}")


if __name__ == "__main__":
    main()
