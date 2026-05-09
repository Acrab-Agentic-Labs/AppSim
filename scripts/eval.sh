#!/usr/bin/env bash
set -Eeuo pipefail

# =============================================================================
# 用户配置区：通常只需要修改这一段
# =============================================================================
# 启动方式：
#   bash scripts/eval.sh
#
# 常用调试方式：
#   RUN_TAG=quick_test bash scripts/eval.sh
#   START_INDEX=0 END_INDEX=1 bash scripts/eval.sh

# 修改AgentName
AGENT_NAME="${AGENT_NAME:-AgentCPM-GUI}"

# 下面三个参数通常不需要修改
PYTHON_BIN="${PYTHON_BIN:-python3}"
RUN_TAG="${RUN_TAG:-$(date +%Y%m%d_%H%M%S)}"
RESULT_ROOT="${RESULT_ROOT:-}"

# OpenAI 兼容 API 列表。三组数组按下标一一对应，数量必须不少于设备数量。
# 本地服务如果不校验 key，也需要显式填写一个占位值，例如 EMPTY。
API_BASES=(
  "your-api-base-url-1"
  "your-api-base-url-2"
  "your-api-base-url-3"
  "your-api-base-url-4"
)
API_KEYS=(
  "your-api-key-1"
  "your-api-key-2"
  "your-api-key-3"
  "your-api-key-4"
)
MODEL_NAMES=(
  "your-model-name-1"
  "your-model-name-2"
  "your-model-name-3"
  "your-model-name-4"
)

# 模型请求参数。当前短上下文服务建议保持默认值。
MAX_TOKENS="${MAX_TOKENS:-512}"
HISTORY_IMAGE_TURNS="${HISTORY_IMAGE_TURNS:-1}"

# Android 设备。可以是远程 host:port，也可以是 emulator-5554 这类本地设备 ID。
DEVICE_IDS=(
  "device-1-address"
  "device-2-address"
  "device-3-address"
  "device-4-address"
)

# 要评测的 App。脚本会按 round-robin 分配到 DEVICE_IDS。
APPS=(
  "GAODE"
  "BILIBILI"
  "CTRIP"
  "ELEME"
  "MYJD"
  "MUSIC"
  "RED_NOTE"
  "TENCENT_MEETING"
  "UBEREATS"
  "WECHAT"
  "YOUTUBE"
  "AMAZON"
  "WHATSAPP"
  "BOOKING"
  "ZOOM"
  "SPOTIFY"
  "INSTAGRAM"
)

# 只跑每个 App 的部分任务时填写；留空表示跑完整任务集。
START_INDEX="${START_INDEX:-}"
END_INDEX="${END_INDEX:-}"

# 每个 App 失败后的总尝试次数。2 表示首跑一次、失败后重试一次。
MAX_APP_ATTEMPTS="${MAX_APP_ATTEMPTS:-2}"

# 下面加载固定执行逻辑。一般不需要改。
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/eval_runner.bash"