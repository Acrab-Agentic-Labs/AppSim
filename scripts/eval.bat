@REM Windows CMD脚本
@REM 适用于 Windows 系统

@echo off

set API_BASE=https://ark.cn-beijing.volces.com/api/v3
set API_KEY=
set MODEL_NAME=doubao-1-5-ui-tars-250428

set agent_name=UI-TARS-1.5
set device_id=emulator-5554

python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task BILIBILI
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task CTRIP
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task ELEME
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task GAODE
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task MYJD
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task MUSIC
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task RED_NOTE
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task TENCENT_MEETING
python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task WECHAT

