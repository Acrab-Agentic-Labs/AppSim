@REM Windows CMD脚本
@REM 适用于 Windows 系统

@echo off

set API_BASE=https://ark.cn-beijing.volces.com/api/v3
set API_KEY=19be0921-943a-4689-b94a-d0c0be51e244
set MODEL_NAME=doubao-1-5-ui-tars-250428

set agent_name=UI-TARS-1.5
set device_id=emulator-5554

python eval_appsim.py --agent-name %agent_name% --device-id %device_id% --output-dir results/%agent_name%/ --task ELEME


