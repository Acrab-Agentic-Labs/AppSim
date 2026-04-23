#!/usr/bin/env bash
set -Eeuo pipefail

# Fill DEVICE_1..DEVICE_4 with your cloud phone addresses before running.
# Apps are distributed round-robin across 4 devices.
# GAODE is intentionally excluded.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUN_TAG="${RUN_TAG:-$(date +%Y%m%d_%H%M%S)}"
AGENT_NAME="${AGENT_NAME:-UI-TARS-1.5}"
RESULT_ROOT="${RESULT_ROOT:-${SCRIPT_DIR}/results/${AGENT_NAME}/${RUN_TAG}}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
ERROR_LOG=""

# ============================================================================
# API Configuration (REQUIRED)
# ============================================================================
# Set these environment variables before running, or modify the defaults below:
API_BASE="${API_BASE:-https://your-api-endpoint.com/api/v3}"
API_KEY="${API_KEY:-your-api-key-here}"

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
# The array size must match the number of devices (currently 4).
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
# Format: "host:port" for remote devices, or "emulator-5554" for local emulators
DEVICE_IDS=(
  "device-1-host:port"
  "device-2-host:port"
  "device-3-host:port"
  "device-4-host:port"
)

APPS=(
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

  mkdir -p "${app_output_dir}"
  : > "${log_path}"

  echo "[$(date '+%F %T')] Starting ${app} on ${device}"

  set +e
  "${PYTHON_BIN}" "${SCRIPT_DIR}/eval_appsim.py" \
    --agent-name "${AGENT_NAME}" \
    --device-id "${device}" \
    --output-dir "${app_output_dir}" \
    --task "${app}" \
    --start-index 0 \
    --end-index 1 \
    > >(tee -a "${log_path}") \
    2> >(tee -a "${log_path}" >&2)
  rc=$?
  set -e

  if [[ "${rc}" -ne 0 ]]; then
    echo "[$(date '+%F %T')] FAILED ${app} on ${device} (exit ${rc})" >&2
  else
    echo "[$(date '+%F %T')] Finished ${app} on ${device}"
  fi

  return "${rc}"
}

run_device_queue() {
  local worker_index="$1"
  local device="$2"
  local app_index
  local failures=0
  local -a failed_apps=()

  # Set device-specific model to avoid rate limiting
  export MODEL_NAME="${MODEL_NAMES[$worker_index]}"
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
