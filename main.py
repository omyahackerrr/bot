import telebot
from handlers import handle_start, handle_new_content
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Command handler
@bot.message_handler(commands=['start'])
def start(message):
    handle_start(bot, message)

# Content forward handler
@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
def forward_content(message):
    handle_new_content(bot, message)

print("🤖 Bot is running...")
bot.polling()
