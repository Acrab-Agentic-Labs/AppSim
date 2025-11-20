# 项目介绍

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
```
# 启动模拟器
# 如果遇到检查的ANDROID_SDK_ROOT路径不对
# 修改 vi ~/.android/avd/testavd2.avd/config.ini 中 image.sysdir.1 的路径为绝对路径或相对 $ANDROID_SDK_ROOT 的路径
emualtor @testavd -no-boot-anim -netdelay none -accel on -no-snapshot -wipe-data -no-window -port 5554
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

```
# adb 连接目标端口
adb connect server_ip:5555

# scrcpy 启动
scrcpy
```

## 评测环境

### 准备工作

```py
uv venv --python=3.11
pip install -r requirments.txt
pip install -e .
```

### 使用说明

#### 1. 基础用法
```bash
python scripts/eval_appsim.py \
    --agent-name UI-TARS-1.5 \
    --task BILIBILI \
    --device-id emulator-5554 \
    --output-dir results/UI-TARS-1.5/

```

#### 2. 参数说明

##### 命令行参数
- `--agent-name`: Agent 名称，可选值：
  - `Seed-1.5-VL`
  - `UI-TARS-1.5`（默认推荐）
  - `GPT-5`
  - `Gemini-2.5-Pro`
  - `Claude-4.5-Sonnet`

- `--task`: 要评估的应用任务，可选值：
  - `BILIBILI` - 哔哩哔哩
  - `CTRIP` - 携程旅行
  - `ELEME` - 饿了么
  - `GAODE` - 高德地图
  - `MYJD` - 京东
  - `MUSIC` - 网易云音乐
  - `RED_NOTE` - 小红书
  - `TENCENT_MEETING` - 腾讯会议
  - `WECHAT` - 微信

- `--device-id`: 设备ID（adb地址），例如：
  - `emulator-5554` - 模拟器
  - `122.228.230.212:10246` - 远程设备

- `--output-dir`: 结果输出目录（默认: `./output/`）

- `--start-index`: 从指定索引开始执行任务（默认: 0）

- `--end-index`: 执行任务的结束索引（默认为None. 非None时按照Python的习惯执行 task_items[start_index:end_index]）

- `--verbose`: 设置时显示详细的log信息(等同于logging.DEBUG)

#### 环境变量
##### 环境变量

```bash
export API_BASE='https://ark.cn-beijing.volces.com/api/v3'
export API_KEY='your-api-key-here'
export MODEL_NAME='doubao-1-5-ui-tars-250428'              # 设置使用的模型名，跟AgentName是两个概念
```

#### 3. 使用 `eval.sh` 或 `eval.bat`

在 `eval.sh`  和 `eval.bat`（For Windows CMD） 中提供了测试脚本的示例用法：

#### 4. 特别说明
- 使用 `UI-TARS-1.5` Agent 时，模型输出的坐标使用 1000x1000 坐标系
- 如果使用其他模型，请确保模型输出的坐标格式符合要求（1000x1000 坐标系，整数坐标）
- 评估结果会实时保存到输出目录的 JSONL 文件中，文件名包含时间戳


##### UITARS官方API提供的手机GUI任务处理场景动作表
> 记录UI-TARS模型的官方API提供的Action
模型会输出类似于`click(point='<point>500 257</point>')`这样的一段动作，我们按照下表展示的规则去解析模型输出的内容。

| Action 名称 | 动作类型 | 参数                | 输出示例                                                                 |
|-------------|----------|---------------------|--------------------------------------------------------------------------|
| click       | 点击     | point               | JSON<br>`click(point='<point>x1 y1</point>')`                            |
| long_press  | 长按     | point               | JSON<br>`long_press(point='<point>x1 y1</point>')`                       |
| type        | 输入     | content             | JSON<br>`type(content='文本内容\\n')`                                    |
| scroll      | 滚动     | point、direction    | JSON<br>`scroll(point='<point>x1 y1</point>', direction='down')`         |
| open_app    | 打开应用 | app_name            | JSON<br>`open_app(app_name='微信')`                                      |
| drag        | 拖拽     | start_point、end_point | JSON<br>`drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')` |
| press_home  | 返回主屏幕 | 无                  | JSON<br>`press_home()`                                                   |
| press_back  | 返回     | 无                  | JSON<br>`press_back()`                                                   |
| finished    | 完成     | content             | JSON<br>`finished(content='操作完成信息')`                                |


### 5. 扩展Agent类型 
项目支持多种 Agent，通过 `--agent-name` 参数切换。不同的 Agent 对应不同的模型和配置，具体实现位于 `scripts/agent_factory/agent_factory.py`。

如果需要添加新的 Agent 或修改模型配置，请编辑 `scripts/agent_factory/agent_factory.py` 文件。
