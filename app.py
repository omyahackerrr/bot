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
    await update.message.reply_text("📥 Send me any media file to upload to Archive.org.")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = None
        filename = "file"
        if update.message.video:
            file = await context.bot.get_file(update.message.video.file_id)
            filename = "video.mp4"
        elif update.message.document:
            file = await context.bot.get_file(update.message.document.file_id)
            filename = update.message.document.file_name or "document"
        elif update.message.audio:
            file = await context.bot.get_file(update.message.audio.file_id)
            filename = "audio.mp3"
        elif update.message.photo:
            file = await context.bot.get_file(update.message.photo[-1].file_id)
            filename = "photo.jpg"
        else:
            await update.message.reply_text("❌ Unsupported media type.")
            return

        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
        response = requests.get(file_url, stream=True)
        if response.status_code != 200:
            await update.message.reply_text("❌ Failed to download file.")
            return

        item_name = f"upload_{update.effective_user.id}_{update.message.message_id}"

        s3 = boto3.resource(
            's3',
            endpoint_url='https://s3.us.archive.org',
            aws_access_key_id=ARCHIVE_ACCESS_KEY,
            aws_secret_access_key=ARCHIVE_SECRET_KEY
        )
        bucket = s3.Bucket(item_name)
        bucket.upload_fileobj(response.raw, filename)

        archive_link = f"https://archive.org/details/{item_name}"
        await update.message.reply_text(f"✅ Uploaded!\n{archive_link}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def run_bot():
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.ALL, handle_media))
    bot.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()

