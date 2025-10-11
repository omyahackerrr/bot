from flask import Flask
import requests, boto3, os, threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

ARCHIVE_ACCESS_KEY = os.getenv("ARCHIVE_ACCESS_KEY")
ARCHIVE_SECRET_KEY = os.getenv("ARCHIVE_SECRET_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send me a video file to upload to Archive.org.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file_id = update.message.video.file_id
        file = await context.bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

        response = requests.get(file_url, stream=True)
        if response.status_code != 200:
            await update.message.reply_text("❌ Failed to download video.")
            return

        item_name = f"upload_{update.effective_user.id}_{update.message.message_id}"

        s3 = boto3.resource(
            's3',
            endpoint_url='https://s3.us.archive.org',
            aws_access_key_id=ARCHIVE_ACCESS_KEY,
            aws_secret_access_key=ARCHIVE_SECRET_KEY
        )
        bucket = s3.Bucket(item_name)
        bucket.upload_fileobj(response.raw, 'video.mp4')

        archive_link = f"https://archive.org/details/{item_name}"
        await update.message.reply_text(f"✅ Uploaded!\n{archive_link}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def run_bot():
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.VIDEO, handle_video))
    bot.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=1.0, close_loop=False)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()
