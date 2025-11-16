# import subprocess
# import json

# def validate_reviews_page(result=None,device_id=None):
#     cmd = ['adb']
#     if device_id:
#         cmd.extend(['-s', device_id])
#     cmd.extend(['exec-out', 'run-as', 'com.example.myele', 'cat', 'files/messages.json'])
#     subprocess.run(cmd, stdout=open('messages.json', 'w'))

#     try:
#         with open('messages.json', 'r', encoding='utf-8') as f:
#             data = json.load(f)
#             if isinstance(data, list):
#                 data = data[-1] if data else {}
#     except:
#         return False

#     if data.get('action') != 'enter_reviews_page':
#         return False
#     if data.get('page') != 'reviews':
#         return False
#     if 'extra_data' not in data:
#         return False
#     extra_data = data['extra_data']
#     # 【关键】必须选择"待评价"标签
#     if extra_data.get('selected_tab') != '待评价':
#         return False
#     return True

# if __name__ == '__main__':
#     result = validate_reviews_page()
#     print(result)
