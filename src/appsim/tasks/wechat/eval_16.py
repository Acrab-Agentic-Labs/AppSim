# 16、从"发现"进入朋友圈，浏览好友朋友圈，给第一个分享小猫朋友圈的好友和第一个分享小狗朋友圈的好友分别发送"你的猫好可爱！"和"你的狗好可爱！"
import os
import json
import subprocess


def verify_multiple_moment_authors_contacted(result=None, device_id=None, backup_dir=None):
    def _normalize_exclamation(content):
        return str(content).replace("!", "！")

    def _validate_message_send(receiverId, senderId, message_content, device_id, backup_dir):
        try:
            message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

            # adb拿到文件
            cmd = ["adb"]
            if device_id:
                cmd.extend(["-s", device_id])
            cmd.extend(["exec-out", "run-as", "com.example.fakewechat", "cat", "files/messages.json"])

            with open(message_file_path, "w", encoding="utf-8") as f:
                subprocess.run(cmd, stdout=f, check=True)

            # 打开此文件
            with open(message_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 检查聊天记录
            item = data["privateChatMessages"][receiverId][-1]
            if (
                item["senderId"] == senderId
                and _normalize_exclamation(item["content"]) == _normalize_exclamation(message_content)
            ):
                return True
            else:
                return False
        except:
            return False

    _SENDER_ID = "current_user"
    # user_1 (王晨曦) 发了小猫朋友圈
    _CAT_RECEIVER = "user_1"
    _CAT_MESSAGE = "你的猫好可爱！"
    # user_3 (张杰) 发了小狗朋友圈
    _DOG_RECEIVER = "user_3"
    _DOG_MESSAGE = "你的狗好可爱！"

    try:
        return _validate_message_send(
            receiverId=_CAT_RECEIVER, senderId=_SENDER_ID, message_content=_CAT_MESSAGE,
            device_id=device_id, backup_dir=backup_dir
        ) and _validate_message_send(
            receiverId=_DOG_RECEIVER, senderId=_SENDER_ID, message_content=_DOG_MESSAGE,
            device_id=device_id, backup_dir=backup_dir
        )
    except:
        return False


if __name__ == "__main__":
    print(verify_multiple_moment_authors_contacted())
