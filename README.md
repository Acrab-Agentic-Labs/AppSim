# AppSim-Bench: Bridging Real-world Apps and Reproducible Evaluation for Mobile GUI Agents

<p align="center">
<a href="README_CN.md">中文</a> &nbsp; | &nbsp; English
</p>

<p align="center">
<a href="https://acrab-agentic-labs.github.io/AppSim/">Project Homepage</a> &nbsp; | &nbsp; <a href="https://arxiv.org/abs/2609.07712">Paper</a>
</p>

## Contents

- [Project Overview](#project-overview)
- [Environment Setup](#environment-setup)
  - [AVD Emulator](#avd-emulator)
    - [Windows & MacOS](#windows--macos)
    - [Linux Server](#linux-server)
- [Evaluation Setup](#evaluation-setup)
  - [Preparation](#preparation)
    - [Install App APKs](#install-app-apks)
  - [Usage](#usage)
    - [1. Basic Usage](#1-basic-usage)
    - [2. Parameters](#2-parameters)
    - [3. Batch Evaluation Scripts](#3-batch-evaluation-scripts)
    - [4. Notes](#4-notes)
    - [5. Extending Agent Types](#5-extending-agent-types)
- [FAQ](#faq)
- [Citation](#citation)

---

## Project Overview

AppSim is an automated evaluation framework for GUI agents on mobile apps.

## Environment Setup

### AVD Emulator

#### Windows & MacOS

TODO: install through Android Studio.

#### Linux Server

##### Install JDK

```bash
wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz ./
tar -zxvf openjdk-17.0.2_linux-x64_bin.tar.gz -C /opt
export JAVA_HOME="/opt/jdk-17.0.2"
export PATH="$PATH:$JAVA_HOME/bin"
export CLASSPATH=$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
```

##### Install SDKManager

```bash
wget https://dl.google.com/android/repository/commandlinetools-linux-8092744_latest.zip
unzip commandlinetools-linux-8092744_latest.zip -d /opt/
export PATH="$PATH:/opt/cmdline-tools/bin"
```

##### Configure Environment Variables

```bash
export ANDROID_SDK_ROOT=/opt/android-sdk
sdkmanager --sdk_root=$ANDROID_SDK_ROOT --install "platform-tools" "emulator" "build-tools;33.0.0" "platforms;android-33" "system-images;android-33;default;x86_64"
export PATH="$PATH:$ANDROID_SDK_ROOT/emulator:$ANDROID_SDK_ROOT/platform-tools"
```

##### Create Emulator

```bash
avdmanager --verbose create avd --force --name "testavd" --package "system-images;android-33;default;x86_64"
```

##### Start Emulator

```bash
emulator @testavd -no-boot-anim -netdelay none -accel on -no-snapshot -wipe-data -no-window -port 5554
```

If `ANDROID_SDK_ROOT` is checked in the wrong location, update `image.sysdir.1` in `~/.android/avd/testavd.avd/config.ini` to an absolute path or a path relative to `$ANDROID_SDK_ROOT`.

##### View the Emulator Screen with scrcpy (optional)

If you want to view the AVD screen from a local machine, use `scrcpy`.

1. Remote machine setup

```bash
adb tcpip 5555
ufw allow 5555/tcp
```

2. Local machine connection

```bash
adb connect server_ip:5555
scrcpy
```

## Evaluation Setup

### Preparation

#### Install App APKs

Before running evaluations, install the 17 AppSim APKs on the test phone or emulator. You can also fork the source repos below and build the APKs yourself for evaluation.

| Chinese Name | English Name | GitHub Repo |
|---|---|---|
| 哔哩哔哩 | BiliBili | https://github.com/Acrab-Agentic-Labs/AppSim-BiliBili |
| 饿了么 | Eleme | https://github.com/Acrab-Agentic-Labs/AppSim-Eleme |
| 高德地图 | Amap | https://github.com/Acrab-Agentic-Labs/AppSim-Amap |
| 京东 | JD | https://github.com/Acrab-Agentic-Labs/AppSim-JD |
| 腾讯会议 | Tencent Meeting | https://github.com/Acrab-Agentic-Labs/AppSim-TencentMeeting |
| 网易云音乐 | NetEase Cloud Music | https://github.com/Acrab-Agentic-Labs/AppSim-NetEaseCloudMusic |
| 微信 | WeChat | https://github.com/Acrab-Agentic-Labs/AppSim-Wechat-V2 |
| 小红书 | RedNote | https://github.com/Acrab-Agentic-Labs/AppSim-RedNote |
| 携程 | Ctrip | https://github.com/Acrab-Agentic-Labs/AppSim-Ctrip |
|  | Amazon | https://github.com/Acrab-Agentic-Labs/AppSim-Amazon |
|  | Booking | https://github.com/Acrab-Agentic-Labs/AppSim-Booking |
|  | Instagram | https://github.com/Acrab-Agentic-Labs/AppSim-Instagram |
|  | Spotify | https://github.com/Acrab-Agentic-Labs/GUIAgent-Spotify |
|  | Uber Eats | https://github.com/Acrab-Agentic-Labs/AppSim-UberEats |
|  | WhatsApp | https://github.com/Acrab-Agentic-Labs/AppSim-WhatsApp |
|  | YouTube | https://github.com/Acrab-Agentic-Labs/AppSim-Youtube |
|  | Zoom | https://github.com/Acrab-Agentic-Labs/AppSim-Zoom |

```bash
uv venv --python=3.11
pip install -r requirements.txt
pip install -e .
```

### Usage

#### 1. Basic Usage

Single app evaluation:

```bash
python scripts/eval_appsim.py \
    --agent-name AgentCPM-GUI \
    --task BILIBILI \
    --device-id emulator-5554 \
    --output-dir results/AgentCPM-GUI/
```

#### 2. Parameters

##### Command-line arguments

- `--agent-name`: Agent name. Examples:
  - `GPT-5`
  - `AgentCPM-GUI`

  See [`scripts/agent_factory/agent_factory.py`](scripts/agent_factory/agent_factory.py) for the complete list.

- `--task`: App task to evaluate. Available values:
  - `BILIBILI` - BiliBili
  - `CTRIP` - Ctrip
  - `ELEME` - Eleme
  - `GAODE` - Amap
  - `MYJD` - JD
  - `MUSIC` - NetEase Cloud Music
  - `RED_NOTE` - RedNote
  - `TENCENT_MEETING` - Tencent Meeting
  - `UBEREATS` - Uber Eats
  - `WECHAT` - WeChat
  - `YOUTUBE` - YouTube
  - `AMAZON` - Amazon
  - `WHATSAPP` - WhatsApp
  - `BOOKING` - Booking.com
  - `ZOOM` - Zoom
  - `SPOTIFY` - Spotify
  - `INSTAGRAM` - Instagram

- `--device-id`: Device ID (adb address), for example:
  - `emulator-5554` - emulator
  - `122.228.230.212:10246` - remote device

- `--output-dir`: Output directory (default: `./output/`)

- `--start-index`: Start task index (default: `0`)

- `--end-index`: End task index (default: `None`). When not `None`, the script follows Python slicing semantics for `task_items[start_index:end_index]`.

- `--verbose`: Show detailed log output (equivalent to `logging.DEBUG`)

##### Environment variables

When running `scripts/eval_appsim.py` directly, you can configure the OpenAI-compatible API with common environment variables:

```bash
export API_BASE='https://your-api-endpoint.com/api/v3'
export API_KEY='your-api-key-here'
export MODEL_NAME='your-model-name'
```

For tasks with `evaluation_type="answer"` or `evaluation_type="hybrid"`, the evaluation script also calls an answer extractor to structure the agent's `final_message` into `result["extracted_answer"]`. By default, the extractor reuses `API_BASE`, `API_KEY`, and `MODEL_NAME` above. If you want the extractor to use a separate model, configure it explicitly:

```bash
export ANSWER_EXTRACTOR_API_BASE='https://your-extractor-endpoint.com/api/v3'
export ANSWER_EXTRACTOR_API_KEY='your-extractor-api-key'
export ANSWER_EXTRACTOR_MODEL_NAME='your-extractor-model-name'
```

New `answer` and `hybrid` tasks prefer `result["extracted_answer"]` for validation, instead of relying on the legacy `final_message` text format constraint such as `<ans>...</ans>`.

Different agents also support their own environment variable prefixes, such as `AGENTCPM_GUI_API_BASE`, `AGENTCPM_GUI_API_KEY`, and `AGENTCPM_GUI_MODEL_NAME`. Batch scripts export these variables automatically per device, so in most cases you only need to edit the configuration block in `scripts/eval.sh`.

#### 3. Batch Evaluation Scripts

The project provides batch evaluation scripts that can run evaluations for multiple apps in parallel across multiple devices.

##### Using `eval.sh` (Linux/MacOS)

**Step 1: Configure the script**

Edit `scripts/eval.sh` and set the following values:

```bash
AGENT_NAME="<agent-name>"

API_BASES=(
  "https://your-api-endpoint-1.com/api/v3"
  "https://your-api-endpoint-2.com/api/v3"
  "https://your-api-endpoint-3.com/api/v3"
  "https://your-api-endpoint-4.com/api/v3"
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

DEVICE_IDS=(
  "device-1-host:port"
  "device-2-host:port"
  "device-3-host:port"
  "device-4-host:port"
)

APPS=(
  "GAODE"
  "BILIBILI"
  "CTRIP"
)
```

**Step 2: Run the script**

```bash
bash scripts/eval.sh
```

**Features**

- Automatically starts workers in parallel based on `DEVICE_IDS`
- Uses the matching `API_BASES`, `API_KEYS`, and `MODEL_NAMES` entry for each device
- Distributes `APPS` to devices in round-robin order
- Attempts `adb connect` first for remote `host:port` devices
- Retries each app up to `MAX_APP_ATTEMPTS`, and reconnects when uiautomator2 connection errors occur
- Saves `eval_details_*.jsonl`, `run.log`, and `console_errors.log` in real time
- Generates timestamped result directories automatically

**Output structure**

```text
scripts/results/
└── AgentCPM-GUI/
    └── 20260423_001257/          # RUN_TAG, defaults to the run timestamp
        ├── 122.228.230.214_10454/
        │   ├── BILIBILI/
        │   │   ├── eval_details_Bilibili_*.jsonl
        │   │   ├── run.log
        │   │   └── screenshots/
        │   ├── MUSIC/
        │   └── ...
        ├── 122.228.230.214_10455/
        └── console_errors.log
```

##### Using `eval.bat` (Windows)

Windows users can use `eval.bat`. The configuration is similar.

##### Custom Configuration

You can override the default settings with environment variables:

```bash
export AGENT_NAME="GPT-5"
export RESULT_ROOT="./my_results/"
export RUN_TAG="experiment_001"
export START_INDEX=0
export END_INDEX=2
export MAX_APP_ATTEMPTS=2

bash scripts/eval.sh
```

`AgentCPM-GUI` also supports `MAX_TOKENS` and `HISTORY_IMAGE_TURNS` for request tuning. The current short-context service recommends keeping the defaults: `MAX_TOKENS=512` and `HISTORY_IMAGE_TURNS=1`.

#### 4. Notes

- `UI-TARS-1.5` uses a 1000x1000 coordinate system for model outputs
- `AgentCPM-GUI` uses compact JSON and a 0-1000 relative coordinate system
- If you use another model, make sure its coordinate format matches the required 1000x1000 integer coordinate format
- Evaluation results are saved to JSONL files in the output directory in real time, and the file names include timestamps

#### 5. Extending Agent Types

The project supports multiple agents through the `--agent-name` parameter. Different agents map to different models and settings, and the implementation lives in `scripts/agent_factory/agent_factory.py`.

To add a new agent or change model settings, edit `scripts/agent_factory/agent_factory.py`.

---

## FAQ

### Q: How can I monitor evaluation progress?

A: Logs are printed in real time during evaluation:
- Console output: current execution status
- `run.log`: detailed logs for each app
- `console_errors.log`: aggregated error messages

### Q: How do I debug a failed evaluation?

A: Follow these steps:
1. Check `run.log` for the exact error
2. Confirm the device connection: `adb devices`
3. Confirm the API settings are correct (`API_BASE`, `API_KEY`, `MODEL_NAME`)
4. Check `console_errors.log` for global errors

### Q: How do I test only a subset of apps?

A: Edit the `APPS` array in `eval.sh` and keep only the app names you want to test.

## Citation

```bibtex
@misc{appsimbench,
      title={APPSim-Bench: Bridging Real-world Apps and Reproducible Evaluation for Mobile GUI Agents},
      author={Jintian Feng and Long Chen and Xiao Yu and Jiayi Dai and Chenglong Liu and Haoru Wang and Zizhen Xue and Yuxuan Shi and Ziyang Wang and Yichen Gong},
      year={2026},
      eprint={2609.07712},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2609.07712},
}
```

---
