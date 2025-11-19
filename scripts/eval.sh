# /bin/bash
# MacOS 和 Linux 通用脚本

# 设置环境变量
export API_BASE='https://ark.cn-beijing.volces.com/api/v3'
export API_KEY=''
export MODEL_NAME='doubao-1-5-ui-tars-250428'

agent_name=UI-TARS-1.5
device_id=emulator-5554

python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task BILIBILI
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task CTRIP
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task ELEME
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task GAODE  
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task MYJD 
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task MUSIC
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task RED_NOTE
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task TENCENT_MEETING
python eval_appsim.py --agent-name $agent_name --device-id $device_id --output-dir results/$agent_name/ --task WECHAT
