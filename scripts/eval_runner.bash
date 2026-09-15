# -*- bash -*-
# 固定评测执行器。用户通常只需要修改 eval.sh 里的配置区。

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RESULT_ROOT="${RESULT_ROOT:-${SCRIPT_DIR}/results/${AGENT_NAME}/${RUN_TAG}}"
ERROR_LOG=""

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

is_non_negative_int() {
  [[ "$1" =~ ^[0-9]+$ ]]
}

is_positive_int() {
  [[ "$1" =~ ^[1-9][0-9]*$ ]]
}

validate_config() {
  if [[ "${#DEVICE_IDS[@]}" -lt 1 ]]; then
    echo "Please configure at least one device in DEVICE_IDS." >&2
    exit 1
  fi
  if [[ "${#APPS[@]}" -lt 1 ]]; then
    echo "Please configure at least one app in APPS." >&2
    exit 1
  fi

  local device
  for device in "${DEVICE_IDS[@]}"; do
    if [[ -z "${device}" || "${device}" == device-* || "${device}" == *"host:port"* ]]; then
      echo "Please replace every DEVICE_IDS placeholder before running." >&2
      exit 1
    fi
  done

  if [[ "${#API_BASES[@]}" -lt 1 ]]; then
    echo "Please configure at least one api_base in API_BASES." >&2
    exit 1
  fi
  if [[ "${#API_BASES[@]}" -ne "${#API_KEYS[@]}" ]]; then
    echo "API_BASES and API_KEYS must have the same length." >&2
    exit 1
  fi
  if [[ "${#API_BASES[@]}" -ne "${#MODEL_NAMES[@]}" ]]; then
    echo "API_BASES and MODEL_NAMES must have the same length." >&2
    exit 1
  fi
  if [[ "${#API_BASES[@]}" -lt "${#DEVICE_IDS[@]}" ]]; then
    echo "API count must be greater than or equal to device count." >&2
    exit 1
  fi

  local api_index
  for api_index in "${!API_BASES[@]}"; do
    if [[ -z "${API_BASES[$api_index]}" || "${API_BASES[$api_index]}" == your-api-base-url* ]]; then
      echo "Please replace every API_BASES placeholder before running." >&2
      exit 1
    fi
    if [[ -z "${API_KEYS[$api_index]}" || "${API_KEYS[$api_index]}" == your-api-key* ]]; then
      echo "Please replace every API_KEYS placeholder before running." >&2
      exit 1
    fi
    if [[ -z "${MODEL_NAMES[$api_index]}" || "${MODEL_NAMES[$api_index]}" == your-model-name-* ]]; then
      echo "Please replace every MODEL_NAMES placeholder before running." >&2
      exit 1
    fi
  done

  if ! is_positive_int "${MAX_TOKENS}"; then
    echo "MAX_TOKENS must be a positive integer." >&2
    exit 1
  fi
  if ! is_non_negative_int "${HISTORY_IMAGE_TURNS}"; then
    echo "HISTORY_IMAGE_TURNS must be 0 or 1." >&2
    exit 1
  fi
  if [[ "${HISTORY_IMAGE_TURNS}" -gt 1 ]]; then
    echo "HISTORY_IMAGE_TURNS must be 0 or 1 for current 2048 context services." >&2
    exit 1
  fi

  if ! is_positive_int "${MAX_APP_ATTEMPTS}"; then
    echo "MAX_APP_ATTEMPTS must be a positive integer." >&2
    exit 1
  fi
  if [[ -n "${START_INDEX}" ]] && ! is_non_negative_int "${START_INDEX}"; then
    echo "START_INDEX must be empty or a non-negative integer." >&2
    exit 1
  fi
  if [[ -n "${END_INDEX}" ]] && ! is_non_negative_int "${END_INDEX}"; then
    echo "END_INDEX must be empty or a non-negative integer." >&2
    exit 1
  fi
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

eval_args() {
  local -n out_args="$1"
  if [[ -n "${START_INDEX}" ]]; then
    out_args+=(--start-index "${START_INDEX}")
  fi
  if [[ -n "${END_INDEX}" ]]; then
    out_args+=(--end-index "${END_INDEX}")
  fi
}

export_worker_model_config() {
  local worker_index="$1"
  local device="$2"
  local api_index="${worker_index}"

  export API_BASE="${API_BASES[$api_index]}"
  export API_KEY="${API_KEYS[$api_index]}"
  export MODEL_NAME="${MODEL_NAMES[$api_index]}"

  case "${AGENT_NAME}" in
    "Seed-1.5-VL")
      export SEED15_VL_API_BASE="${API_BASE}"
      export SEED15_VL_API_KEY="${API_KEY}"
      export SEED15_VL_MODEL_NAME="${MODEL_NAME}"
      ;;
    "UI-TARS-1.5")
      export UI_TARS_15_API_BASE="${API_BASE}"
      export UI_TARS_15_API_KEY="${API_KEY}"
      export UI_TARS_15_MODEL_NAME="${MODEL_NAME}"
      ;;
    "GPT-5")
      export GPT5_API_BASE="${API_BASE}"
      export GPT5_API_KEY="${API_KEY}"
      export GPT5_MODEL_NAME="${MODEL_NAME}"
      ;;
    "Gemini-2.5-Pro")
      export GEMINI25_PRO_API_BASE="${API_BASE}"
      export GEMINI25_PRO_API_KEY="${API_KEY}"
      export GEMINI25_PRO_MODEL_NAME="${MODEL_NAME}"
      ;;
    "Claude-4.5-Sonnet")
      export CLAUDE45_SONNET_API_BASE="${API_BASE}"
      export CLAUDE45_SONNET_API_KEY="${API_KEY}"
      export CLAUDE45_SONNET_MODEL_NAME="${MODEL_NAME}"
      ;;
    "Qwen3-VL")
      export QWEN3_VL_API_BASE="${API_BASE}"
      export QWEN3_VL_API_KEY="${API_KEY}"
      export QWEN3_VL_MODEL_NAME="${MODEL_NAME}"
      ;;
    "AgentCPM-GUI")
      export AGENTCPM_GUI_API_BASE="${API_BASE}"
      export AGENTCPM_GUI_API_KEY="${API_KEY}"
      export AGENTCPM_GUI_MODEL_NAME="${MODEL_NAME}"
      export AGENTCPM_GUI_MAX_TOKENS="${MAX_TOKENS}"
      export AGENTCPM_GUI_HISTORY_IMAGE_TURNS="${HISTORY_IMAGE_TURNS}"
      ;;
    "OpenSource-UI-TRAS")
      export OPEN_SOURCE_UI_TRAS_API_BASE="${API_BASE}"
      export OPEN_SOURCE_UI_TRAS_API_KEY="${API_KEY}"
      export OPEN_SOURCE_UI_TRAS_MODEL_NAME="${MODEL_NAME}"
      export OPEN_SOURCE_UI_TRAS_MAX_TOKENS="${MAX_TOKENS}"
      export OPEN_SOURCE_UI_TRAS_HISTORY_TURNS="${OPEN_SOURCE_UI_TRAS_HISTORY_TURNS:-8}"
      export OPEN_SOURCE_UI_TRAS_THOUGHT_LANGUAGE="${OPEN_SOURCE_UI_TRAS_THOUGHT_LANGUAGE:-English}"
      export OPEN_SOURCE_UI_TRAS_REQUEST_TIMEOUT_SECONDS="${OPEN_SOURCE_UI_TRAS_REQUEST_TIMEOUT_SECONDS:-300}"
      export OPEN_SOURCE_UI_TRAS_CODE_DIR="${OPEN_SOURCE_UI_TRAS_CODE_DIR:-${ROOT_DIR}/../ModelRepos/UI-TARS/codes}"
      ;;
    "MobileAgent-v3.5")
      export MOBILE_AGENT_V35_API_BASE="${API_BASE}"
      export MOBILE_AGENT_V35_API_KEY="${API_KEY}"
      export MOBILE_AGENT_V35_MODEL_NAME="${MODEL_NAME}"
      export MOBILE_AGENT_V35_MAX_TOKENS="${MOBILE_AGENT_V35_MAX_TOKENS:-${MAX_TOKENS}}"
      export MOBILE_AGENT_V35_REQUEST_TIMEOUT_SECONDS="${MOBILE_AGENT_V35_REQUEST_TIMEOUT_SECONDS:-300}"
      export MOBILE_AGENT_V35_CODE_DIR="${MOBILE_AGENT_V35_CODE_DIR:-${ROOT_DIR}/../ModelRepos/MobileAgent/Mobile-Agent-v3.5/android_world_v3.5}"
      export MOBILE_AGENT_V35_MAX_STEPS="${MOBILE_AGENT_V35_MAX_STEPS:-50}"
      export MOBILE_AGENT_V35_WAIT_AFTER_ACTION_SECONDS="${MOBILE_AGENT_V35_WAIT_AFTER_ACTION_SECONDS:-3}"
      ;;
    "V-Droid")
      export VDROID_VERIFIER_API_BASE="${API_BASE}"
      export VDROID_HELPER_API_BASE="${VDROID_HELPER_API_BASES[${api_index}]}"
      export VDROID_HELPER_API_KEY="${VDROID_HELPER_API_KEYS[${api_index}]}"
      export VDROID_HELPER_MODEL_NAME="${VDROID_HELPER_MODEL_NAMES[${api_index}]}"
      export VDROID_CODE_DIR="${VDROID_CODE_DIR:-${ROOT_DIR}/../ModelRepos/V-Droid}"
      export VDROID_MAX_STEPS="${VDROID_MAX_STEPS:-50}"
      export VDROID_ACTION_COMPLETION_ATTEMPTS="${VDROID_ACTION_COMPLETION_ATTEMPTS:-3}"
      export VDROID_WAIT_AFTER_ACTION_SECONDS="${VDROID_WAIT_AFTER_ACTION_SECONDS:-2}"
      export VDROID_VERIFIER_TIMEOUT_SECONDS="${VDROID_VERIFIER_TIMEOUT_SECONDS:-300}"
      export VDROID_HELPER_TIMEOUT_SECONDS="${VDROID_HELPER_TIMEOUT_SECONDS:-300}"
      export VDROID_HELPER_MAX_TOKENS="${VDROID_HELPER_MAX_TOKENS:-512}"
      export VDROID_VERIFIER_BATCH_SIZE="${VDROID_VERIFIER_BATCH_SIZE:-64}"
      export VDROID_SUMMARY_MODE="${VDROID_SUMMARY_MODE:-llm}"
      export VDROID_HISTORY_TURNS="${VDROID_HISTORY_TURNS:-20}"
      export VDROID_ALLOW_APP_SWITCH="${VDROID_ALLOW_APP_SWITCH:-0}"
      export VDROID_STAGNATION_LIMIT="${VDROID_STAGNATION_LIMIT:-50}"
      export VDROID_REVIEW_TERMINAL_ACTIONS="${VDROID_REVIEW_TERMINAL_ACTIONS:-1}"
      export VDROID_DEVICE_CONNECT_ATTEMPTS="${VDROID_DEVICE_CONNECT_ATTEMPTS:-3}"
      export VDROID_DEVICE_CONNECT_RETRY_SECONDS="${VDROID_DEVICE_CONNECT_RETRY_SECONDS:-2}"
      ;;
  esac

  echo "[Device ${device}] API #$((api_index + 1)): ${API_BASE} (${MODEL_NAME})"
}

print_run_plan() {
  local idx device app
  echo "Run tag: ${RUN_TAG}"
  echo "Agent: ${AGENT_NAME}"
  echo "Results: ${RESULT_ROOT}"
  echo "Devices: ${DEVICE_IDS[*]}"
  echo "API count: ${#API_BASES[@]}"
  echo "Apps: ${APPS[*]}"
  if [[ -n "${START_INDEX}${END_INDEX}" ]]; then
    echo "Task slice: start=${START_INDEX:-0}, end=${END_INDEX:-all}"
  fi
  echo "Device APIs:"
  for idx in "${!DEVICE_IDS[@]}"; do
    device="${DEVICE_IDS[$idx]}"
    echo "  ${device} -> API #$((idx + 1)): ${API_BASES[$idx]} (${MODEL_NAMES[$idx]})"
  done
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
  local -a extra_args=()

  eval_args extra_args
  mkdir -p "${app_output_dir}"
  : > "${log_path}"

  while true; do
    echo "[$(date '+%F %T')] ${app} on ${device}, attempt ${attempt}/${MAX_APP_ATTEMPTS}"
    set +e
    "${PYTHON_BIN}" "${SCRIPT_DIR}/eval_appsim.py" \
      --agent-name "${AGENT_NAME}" \
      --device-id "${device}" \
      --output-dir "${app_output_dir}" \
      --task "${app}" \
      "${extra_args[@]}" \
      > >(tee -a "${log_path}") \
      2> >(tee -a "${log_path}" >&2)
    rc=$?
    set -e

    if [[ "${rc}" -eq 0 ]]; then
      echo "[$(date '+%F %T')] Finished ${app} on ${device}"
      return 0
    fi

    echo "[$(date '+%F %T')] FAILED ${app} on ${device} (exit ${rc})" >&2
    if [[ "${attempt}" -ge "${MAX_APP_ATTEMPTS}" ]]; then
      return "${rc}"
    fi

    if is_uiautomator2_connection_failure "${log_path}"; then
      echo "[$(date '+%F %T')] Detected uiautomator2 connection issue; reconnecting after 3s." >&2
      sleep 3
      maybe_connect_device "${device}"
    fi
    attempt=$((attempt + 1))
  done
}

run_device_queue() {
  local worker_index="$1"
  local device="$2"
  local app_index
  local failures=0
  local -a failed_apps=()

  export_worker_model_config "${worker_index}" "${device}"
  maybe_connect_device "${device}"

  for ((app_index=worker_index; app_index<${#APPS[@]}; app_index+=${#DEVICE_IDS[@]})); do
    if ! run_one_app "${device}" "${APPS[$app_index]}"; then
      failures=$((failures + 1))
      failed_apps+=("${APPS[$app_index]}")
      echo "[$(date '+%F %T')] Continuing after ${APPS[$app_index]} failed on ${device}." >&2
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

  validate_config
  require_cmd adb
  resolve_python

  export PYTHONPATH="${ROOT_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}"
  mkdir -p "${RESULT_ROOT}"
  ERROR_LOG="${RESULT_ROOT}/console_errors.log"
  : > "${ERROR_LOG}"
  exec 3>&2
  exec 2> >(tee -a "${ERROR_LOG}" >&3)

  print_run_plan
  for idx in "${!DEVICE_IDS[@]}"; do
    run_device_queue "${idx}" "${DEVICE_IDS[$idx]}" &
    pids+=("$!")
  done

  for idx in "${!pids[@]}"; do
    if ! wait "${pids[$idx]}"; then
      overall_status=1
    fi
  done

  if [[ "${overall_status}" -eq 0 ]]; then
    echo "All app runs finished. Results are under ${RESULT_ROOT}."
  else
    echo "Completed with failures. Check logs under ${RESULT_ROOT}." >&2
  fi
  return "${overall_status}"
}

main "$@"
