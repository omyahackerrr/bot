from flask import Flask, request, jsonify
import requests, boto3, os, asyncio
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
    await update.message.reply_text("Send me a video file to upload to Archive.org.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file_id = update.message.video.file_id
        file = await context.bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

        response = requests.get(file_url, stream=True)
        if response.status_code != 200:
            await update.message.reply_text("❌ Failed to download video.")
            return

        item_name = "upload_" + str(update.effective_user.id) + "_" + str(update.message.message_id)

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

async def run_bot():
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.VIDEO, handle_video))
    await bot.run_polling()

async def main():
    asyncio.create_task(run_bot())
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

if __name__ == '__main__':
    asyncio.run(main())
