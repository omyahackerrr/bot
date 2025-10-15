import os
from db import is_verified, get_verified_users, save_user

ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))

GROUP_LINKS = [
    "https://t.me/omyahackerrealowner",
    "https://t.me/viralvideolivee",
    "https://whatsapp.com/channel/0029VbB1ipg8PgsKXVp2TY14"
]

def handle_start(bot, message):
    user_id = message.from_user.id
    if is_verified(user_id):
        bot.send_message(user_id, "✅ Verified! Here are your group links:")
        for link in GROUP_LINKS:
            bot.send_message(user_id, link)
    else:
        bot.send_message(user_id, "🔒 Please verify first at: https://your-frontend-url.com")

def handle_new_content(bot, message):
    if message.chat.id == ADMIN_GROUP_ID:
        for user_id in get_verified_users():
            try:
                bot.forward_message(user_id, message.chat.id, message.message_id)
            except:
                pass
