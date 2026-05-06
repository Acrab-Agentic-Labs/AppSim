#!/usr/bin/env bash
# 开始执行之前，请完成全部TODO
set -Eeuo pipefail

# Fill DEVICE_1..DEVICE_4 with your cloud phone addresses before running.
# Apps are distributed round-robin across 4 devices.
# Each app runs all available task items.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUN_TAG="${RUN_TAG:-$(date +%Y%m%d_%H%M%S)}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
ERROR_LOG=""

# TODO
AGENT_NAME="${AGENT_NAME:-UI-TARS-1.5}"
RESULT_ROOT="${RESULT_ROOT:-${SCRIPT_DIR}/results/${AGENT_NAME}/${RUN_TAG}}"


# ============================================================================
# API Configuration (REQUIRED)
# ============================================================================
# TODO: Set these environment variables before running, or modify the defaults below:
API_BASE="your-api-base-url"
API_KEY="your-api-key"

# ============================================================================
# Model Configuration (REQUIRED)
# ============================================================================
# Configure model endpoints for each device to avoid API rate limiting.
#
# Option 1: If you have MULTIPLE model endpoints (recommended for parallel execution)
#   - Assign a different model to each device to distribute API load
#   - Example: Each device uses a different endpoint ID
#
# Option 2: If you only have ONE model endpoint
#   - Use the same model name for all devices
#   - Example: All entries set to "your-model-name"
#
# TODO: The array size must match the number of devices (currently 4).
MODEL_NAMES=(
  "your-model-name-1"  # Used by device 1
  "your-model-name-2"  # Used by device 2
  "your-model-name-3"  # Used by device 3
  "your-model-name-4"  # Used by device 4
)

# ============================================================================
# Device Configuration (REQUIRED)
# ============================================================================
# Configure your Android device addresses here.
# TODO: Format: "host:port" for remote devices, or "emulator-5554" for local emulators
DEVICE_IDS=(
  "device-1-address"
  "device-2-address"
  "device-3-address"
  "device-4-address"
)

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

require_cmd() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
}

resolve_python() {
  if command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    return
  fi

  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
    return
  fi

  echo "Could not find ${PYTHON_BIN} or python in PATH." >&2
  exit 1
}

validate_devices() {
  if [[ "${#DEVICE_IDS[@]}" -ne 4 ]]; then
    echo "Expected exactly 4 device entries." >&2
    exit 1
  fi

  local device
  for device in "${DEVICE_IDS[@]}"; do
    if [[ -z "${device}" || "${device}" == *"cloud-phone-"* || "${device}" == *"host:port"* ]]; then
      echo "Please replace every DEVICE_1..DEVICE_4 placeholder before running." >&2
      exit 1
    fi
  done
}

maybe_connect_device() {
  local device="$1"

  if [[ "${device}" == *:* && "${device}" != emulator-* ]]; then
    echo "Connecting adb to ${device}..."
    adb connect "${device}" >/dev/null || true
  fi
}

is_uiautomator2_connection_failure() {
  local log_path="$1"

  grep -Eiq "uiautomator2.*(连接失败|connect|connection|failed|error)|RemoteDisconnected|HTTPConnectionPool|Max retries exceeded" "${log_path}"
}

print_assignment_plan() {
  local idx device app

  echo "Run tag: ${RUN_TAG}"
  echo "Agent: ${AGENT_NAME}"
  echo "Results: ${RESULT_ROOT}"
  echo "Assignments:"

  for idx in "${!APPS[@]}"; do
    device="${DEVICE_IDS[$((idx % ${#DEVICE_IDS[@]}))]}"
    app="${APPS[$idx]}"
    echo "  ${app} -> ${device}"
  done
}

run_one_app() {
  local device="$1"
  local app="$2"
  local device_slug="${device//[:\/]/_}"
  local app_output_dir="${RESULT_ROOT}/${device_slug}/${app}"
  local log_path="${app_output_dir}/run.log"
  local rc
  local attempt=1
  local max_attempts=2

  mkdir -p "${app_output_dir}"
  : > "${log_path}"

  while true; do
    if [[ "${attempt}" -eq 1 ]]; then
      echo "[$(date '+%F %T')] Starting ${app} on ${device}"
    else
      echo "[$(date '+%F %T')] Retrying ${app} on ${device} (attempt ${attempt}/${max_attempts})"
    fi

    # TODO: 下面的start和end index两行是为了测试用的，正式运行时可以直接删除
    # --start-index 0 \
    # --end-index 2 \
    set +e
    "${PYTHON_BIN}" "${SCRIPT_DIR}/eval_appsim.py" \
      --agent-name "${AGENT_NAME}" \
      --device-id "${device}" \
      --output-dir "${app_output_dir}" \
      --task "${app}" \
      > >(tee -a "${log_path}") \
      2> >(tee -a "${log_path}" >&2)
    rc=$?
    set -e

    if [[ "${rc}" -eq 0 ]]; then
      echo "[$(date '+%F %T')] Finished ${app} on ${device}"
      return 0
    fi

    echo "[$(date '+%F %T')] FAILED ${app} on ${device} (exit ${rc})" >&2

    # 每个 App 非 0 退出只重试一次；连接类失败先等 3 秒并重连设备。
    if [[ "${attempt}" -lt "${max_attempts}" ]]; then
      if is_uiautomator2_connection_failure "${log_path}"; then
        echo "[$(date '+%F %T')] Detected uiautomator2 connection failure for ${app} on ${device}; retrying after 3s." >&2
        sleep 3
        maybe_connect_device "${device}"
      else
        echo "[$(date '+%F %T')] Retrying failed app ${app} on ${device} once." >&2
      fi

      attempt=$((attempt + 1))
      continue
    fi

    return "${rc}"
  done
}

run_device_queue() {
  local worker_index="$1"
  local device="$2"
  local app_index
  local failures=0
  local -a failed_apps=()

  # Set device-specific model to avoid rate limiting
  export MODEL_NAME="${MODEL_NAMES[$worker_index]}"
  export UI_TARS_15_API_BASE="${API_BASE}"
  export UI_TARS_15_API_KEY="${API_KEY}"
  export UI_TARS_15_MODEL_NAME="${MODEL_NAME}"
  echo "[Device ${device}] Using model: ${MODEL_NAME}"

  maybe_connect_device "${device}"

  for ((app_index=worker_index; app_index<${#APPS[@]}; app_index+=${#DEVICE_IDS[@]})); do
    if ! run_one_app "${device}" "${APPS[$app_index]}"; then
      failures=$((failures + 1))
      failed_apps+=("${APPS[$app_index]}")
      echo "[$(date '+%F %T')] Continuing to next app on ${device} after ${APPS[$app_index]} failed." >&2
      continue
    fi
  done

  if [[ "${failures}" -gt 0 ]]; then
    echo "[$(date '+%F %T')] ${device} finished with ${failures} failed app(s): ${failed_apps[*]}" >&2
  fi

  return "${failures}"
}

main() {
  local idx
  local overall_status=0
  local -a pids=()

  require_cmd adb
  resolve_python
  validate_devices

  export PYTHONPATH="${ROOT_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}"
  export API_BASE API_KEY MODEL_NAME
  mkdir -p "${RESULT_ROOT}"
  ERROR_LOG="${RESULT_ROOT}/console_errors.log"
  : > "${ERROR_LOG}"
  exec 3>&2
  exec 2> >(tee -a "${ERROR_LOG}" >&3)

  print_assignment_plan

  for idx in "${!DEVICE_IDS[@]}"; do
    run_device_queue "${idx}" "${DEVICE_IDS[$idx]}" &
    pids+=("$!")
  done

  for idx in "${!pids[@]}"; do
    if ! wait "${pids[$idx]}"; then
      overall_status=1
    fi
  done

  if [[ "${overall_status}" -ne 0 ]]; then
    echo "Completed with failures. Check logs under ${RESULT_ROOT}." >&2
  else
    echo "All app runs finished. Results are under ${RESULT_ROOT}."
  fi

  return "${overall_status}"
}

main "$@"
