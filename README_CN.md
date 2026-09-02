# AppSim 项目文档

## 📑 目录

- [项目介绍](#项目介绍)
- [设备环境](#设备环境)
  - [AVD模拟器](#avd模拟器)
    - [Windows & MacOS](#windows--macos)
    - [Linux服务器](#linux服务器)
- [评测环境](#评测环境)
  - [准备工作](#准备工作)
    - [安装 App APK](#安装-app-apk)
  - [使用说明](#使用说明)
    - [1. 基础用法](#1-基础用法)
    - [2. 参数说明](#2-参数说明)
    - [3. 批量评测脚本](#3-批量评测脚本)
    - [4. 特别说明](#4-特别说明)
    - [5. 扩展Agent类型](#5-扩展agent类型)
- [常见问题](#常见问题)

---

## 项目介绍

AppSim 是一个用于评测 GUI Agent 在移动应用上的自动化测试框架。

## 设备环境

### AVD模拟器

#### Windows & MacOS

TODO: 使用 AndroidStudio 安装

#### Linux服务器

##### 安装JDK

``` bash 
# 下载 JDK
wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz ./

# 解压 JDK
tar -zxvf openjdk-17.0.2_linux-x64_bin.tar.gz -C /opt

# 配置环境变量
export JAVA_HOME="/opt/jdk-17.0.2"
export PATH="$PATH:$JAVA_HOME/bin"
export CLASSPATH=$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
```


##### 安装 SDKManager

```bash
# 下载
wget https://dl.google.com/android/repository/commandlinetools-linux-8092744_latest.zip

# 安装
unzip commandlinetools-linux-8092744_latest.zip -d /opt/

# 配置环境变量
export PATH="$PATH:/opt/cmdline-tools/bin"
```


##### 环境变量配置

```bash
# 配置环境变量
export ANDROID_SDK_ROOT=/opt/android-sdk

# 安装 platform-tools, emulator, build-tools, platforms, system-image
# licenses 全部选 TRUE
sdkmanager --sdk_root=$ANDROID_SDK_ROOT --install "platform-tools" "emulator" "build-tools;33.0.0" "platforms;android-33" "system-images;android-33;default;x86_64"

# 配置环境变量
export PATH="$PATH:$ANDROID_SDK_ROOT/emulator:$ANDROID_SDK_ROOT/platform-tools"
```


##### 创建模拟器
```bash
# 创建 AVD
# 是否创建选no
avdmanager --verbose create avd --force --name "testavd" --package "system-images;android-33;default;x86_64"
```

##### 启动模拟器
```bash
# 启动模拟器
# 如果遇到检查的ANDROID_SDK_ROOT路径不对
# 修改 vi ~/.android/avd/testavd.avd/config.ini 中 image.sysdir.1 的路径为绝对路径或相对 $ANDROID_SDK_ROOT 的路径
emulator @testavd -no-boot-anim -netdelay none -accel on -no-snapshot -wipe-data -no-window -port 5554
```

##### 利用 scrcpy 查看界面内容(可选)

如果需要在本地电脑查看服务器上AVD的页面，可以通过 scrcpy 实现.

1. 远程开发机配置

```bash
# 开启tcpip服务
adb tcpip 5555

# 防火墙允许5555的tcp请求
ufw allow 5555/tcp
```

2. 本地电脑连接

```bash
# adb 连接目标端口
adb connect server_ip:5555

# scrcpy 启动
scrcpy
```

## 评测环境

### 准备工作

#### 安装 App APK

在运行评测前，需要先将 AppSim 依赖的 17 个 App APK 下载并安装到测试手机或模拟器中。你也可以基于下列项目源码进行二次开发，再自行构建 APK 用于评测。

| 中文名 | 英文名 | App 的 GitHub 地址 |
|---|---|---|
| 哔哩哔哩 | BiliBili | https://github.com/Acrab-Lab/AppSim-BiliBili |
| 饿了么 | Eleme | https://github.com/Acrab-Lab/AppSim-Eleme |
| 高德地图 | Amap | https://github.com/Acrab-Lab/AppSim-Amap |
| 京东 | JD | https://github.com/Acrab-Lab/AppSim-JD |
| 腾讯会议 | Tencent Meeting | https://github.com/Acrab-Lab/AppSim-TencentMeeting |
| 网易云音乐 | NetEase Cloud Music | https://github.com/Acrab-Lab/AppSim-NetEaseCloudMusic |
| 微信 | WeChat | https://github.com/Acrab-Lab/AppSim-Wechat-V2 |
| 小红书 | RedNote | https://github.com/Acrab-Lab/AppSim-RedNote |
| 携程 | Ctrip | https://github.com/Acrab-Lab/AppSim-Ctrip |
|  | Amazon | https://github.com/Acrab-Lab/AppSim-Amazon |
|  | Booking | https://github.com/Acrab-Lab/AppSim-Booking |
|  | Instagram | https://github.com/Acrab-Lab/AppSim-Instagram |
|  | Spotify | https://github.com/Acrab-Lab/GUIAgent-Spotify |
|  | Uber Eats | https://github.com/Acrab-Lab/AppSim-UberEats |
|  | WhatsApp | https://github.com/Acrab-Lab/AppSim-WhatsApp |
|  | YouTube | https://github.com/Acrab-Lab/AppSim-Youtube |
|  | Zoom | https://github.com/Acrab-Lab/AppSim-Zoom |

```bash
# 创建虚拟环境
uv venv --python=3.11

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

### 使用说明

#### 1. 基础用法

**单个应用评测**：

```bash
python scripts/eval_appsim.py \
    --agent-name AgentCPM-GUI \
    --task BILIBILI \
    --device-id emulator-5554 \
    --output-dir results/AgentCPM-GUI/
```

#### 2. 参数说明

##### 命令行参数

- `--agent-name`: Agent 名称，可选值：
  - `Seed-1.5-VL`
  - `UI-TARS-1.5`
  - `GPT-5`
  - `Gemini-2.5-Pro`
  - `Claude-4.5-Sonnet`
  - `Qwen3-VL`
  - `AgentCPM-GUI`（批量脚本默认）

- `--task`: 要评估的应用任务，可选值：
  - `BILIBILI` - 哔哩哔哩
  - `CTRIP` - 携程旅行
  - `ELEME` - 饿了么
  - `GAODE` - 高德地图
  - `MYJD` - 京东
  - `MUSIC` - 网易云音乐
  - `RED_NOTE` - 小红书
  - `TENCENT_MEETING` - 腾讯会议
  - `UBEREATS` - Uber Eats
  - `WECHAT` - 微信
  - `YOUTUBE` - YouTube
  - `AMAZON` - Amazon
  - `WHATSAPP` - WhatsApp
  - `BOOKING` - Booking.com
  - `ZOOM` - Zoom
  - `SPOTIFY` - Spotify
  - `INSTAGRAM` - Instagram

- `--device-id`: 设备ID（adb地址），例如：
  - `emulator-5554` - 模拟器
  - `122.228.230.212:10246` - 远程设备

- `--output-dir`: 结果输出目录（默认: `./output/`）

- `--start-index`: 从指定索引开始执行任务（默认: 0）

- `--end-index`: 执行任务的结束索引（默认为None. 非None时按照Python的习惯执行 task_items[start_index:end_index]）

- `--verbose`: 设置时显示详细的log信息(等同于logging.DEBUG)

##### 环境变量

直接运行 `scripts/eval_appsim.py` 时，可以通过通用环境变量提供 OpenAI 兼容接口配置：

```bash
export API_BASE='https://your-api-endpoint.com/api/v3'
export API_KEY='your-api-key-here'
export MODEL_NAME='your-model-name'
```

对于 `evaluation_type="answer"` 或 `evaluation_type="hybrid"` 的任务，评测脚本还会调用 answer extractor，把 agent 的 `final_message` 结构化为 `result["extracted_answer"]`。默认情况下，answer extractor 会复用上面的 `API_BASE`、`API_KEY`、`MODEL_NAME`。如果希望 extractor 使用独立模型，也可以单独配置：

```bash
export ANSWER_EXTRACTOR_API_BASE='https://your-extractor-endpoint.com/api/v3'
export ANSWER_EXTRACTOR_API_KEY='your-extractor-api-key'
export ANSWER_EXTRACTOR_MODEL_NAME='your-extractor-model-name'
```

新接入的 `answer` / `hybrid` 任务会优先读取 `result["extracted_answer"]` 做验证，不再依赖旧的 `final_message` 文本格式约束（例如 `<ans>...</ans>`）。

不同 Agent 也支持自己的环境变量前缀，例如 `AGENTCPM_GUI_API_BASE`、`AGENTCPM_GUI_API_KEY`、`AGENTCPM_GUI_MODEL_NAME`。批量脚本会按设备自动导出这些变量，一般只需要改 `scripts/eval.sh` 的配置区。

#### 3. 批量评测脚本

项目提供了批量评测脚本，可以在多个设备上并行运行所有应用的评测。

##### 使用 `eval.sh` (Linux/MacOS)

**步骤 1：配置脚本**

编辑 `scripts/eval.sh` 文件，配置以下信息：

```bash
# Agent 配置，默认使用 AgentCPM-GUI。
AGENT_NAME="${AGENT_NAME:-AgentCPM-GUI}"

# OpenAI 兼容 API 配置。三组数组按下标一一对应，数量必须不少于设备数量。
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

# Android 设备，可以是远程 host:port，也可以是 emulator-5554。
DEVICE_IDS=(
  "device-1-host:port"
  "device-2-host:port"
  "device-3-host:port"
  "device-4-host:port"
)

# 要评测的 App。脚本会按 round-robin 分配到 DEVICE_IDS。
APPS=(
  "GAODE"
  "BILIBILI"
  "CTRIP"
)
```

**步骤 2：运行脚本**

```bash
bash scripts/eval.sh
```

**特性**：
- 自动按 `DEVICE_IDS` 并行启动 worker
- 每个设备使用对应下标的 `API_BASES`、`API_KEYS`、`MODEL_NAMES`
- Round-robin 方式分配 `APPS` 到设备
- 远程 `host:port` 设备会先尝试 `adb connect`
- 每个 App 失败后按 `MAX_APP_ATTEMPTS` 重试，并在 uiautomator2 连接异常时重连
- 实时保存 `eval_details_*.jsonl`、`run.log` 和 `console_errors.log`
- 自动生成带时间戳的结果目录

**输出结构**：
```
scripts/results/
└── AgentCPM-GUI/
    └── 20260423_001257/          # RUN_TAG，默认是运行时间戳
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

##### 使用 `eval.bat` (Windows)

Windows 用户可以使用 `eval.bat` 脚本，配置方式类似。

##### 自定义配置

可以通过环境变量覆盖默认配置：

```bash
# 自定义 Agent 名称。
export AGENT_NAME="GPT-5"

# 自定义结果目录。
export RESULT_ROOT="./my_results/"

# 自定义运行标签。
export RUN_TAG="experiment_001"

# 只跑每个 App 的部分任务，区间规则同 Python 切片 task_items[start:end]。
export START_INDEX=0
export END_INDEX=2

# 设置每个 App 的总尝试次数。
export MAX_APP_ATTEMPTS=2

bash scripts/eval.sh
```

`AgentCPM-GUI` 还可以通过 `MAX_TOKENS` 和 `HISTORY_IMAGE_TURNS` 控制请求参数。当前短上下文服务建议保持默认值：`MAX_TOKENS=512`、`HISTORY_IMAGE_TURNS=1`。

#### 4. 特别说明

- 使用 `UI-TARS-1.5` Agent 时，模型输出的坐标使用 1000x1000 坐标系
- 使用 `AgentCPM-GUI` Agent 时，模型输出紧凑 JSON，坐标使用 0-1000 相对坐标系
- 如果使用其他模型，请确保模型输出的坐标格式符合要求（1000x1000 坐标系，整数坐标）
- 评估结果会实时保存到输出目录的 JSONL 文件中，文件名包含时间戳

##### UI-TARS 官方 API 提供的手机 GUI 任务处理场景动作表

> 记录 UI-TARS 模型的官方 API 提供的 Action

模型会输出类似于 `click(point='<point>500 257</point>')` 这样的一段动作，我们按照下表展示的规则去解析模型输出的内容。

| Action 名称 | 动作类型 | 参数                | 输出示例                                                                 |
|-------------|----------|---------------------|--------------------------------------------------------------------------|
| click       | 点击     | point               | `click(point='<point>x1 y1</point>')`                            |
| long_press  | 长按     | point               | `long_press(point='<point>x1 y1</point>')`                       |
| type        | 输入     | content             | `type(content='文本内容\\n')`                                    |
| scroll      | 滚动     | point、direction    | `scroll(point='<point>x1 y1</point>', direction='down')`         |
| open_app    | 打开应用 | app_name            | `open_app(app_name='微信')`                                      |
| drag        | 拖拽     | start_point、end_point | `drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')` |
| press_home  | 返回主屏幕 | 无                  | `press_home()`                                                   |
| press_back  | 返回     | 无                  | `press_back()`                                                   |
| finished    | 完成     | content             | `finished(content='操作完成信息')`                                |

#### 5. 扩展Agent类型

项目支持多种 Agent，通过 `--agent-name` 参数切换。不同的 Agent 对应不同的模型和配置，具体实现位于 `scripts/agent_factory/agent_factory.py`。

如果需要添加新的 Agent 或修改模型配置，请编辑 `scripts/agent_factory/agent_factory.py` 文件。

---

## 常见问题

### Q: 如何查看评测进度？

A: 评测过程中会实时输出日志，可以通过以下方式查看：
- 控制台输出：实时显示当前执行状态
- `run.log`：每个应用的详细执行日志
- `console_errors.log`：所有错误信息汇总

### Q: 评测失败如何排查？

A: 按以下步骤排查：
1. 检查 `run.log` 查看具体错误信息
2. 确认设备连接正常：`adb devices`
3. 确认 API 配置正确（API_BASE, API_KEY, MODEL_NAME）
4. 查看 `console_errors.log` 了解全局错误

### Q: 如何只测试部分应用？

A: 编辑 `eval.sh` 中的 `APPS` 数组，只保留需要测试的应用名称。

---
