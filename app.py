from flask import Flask, request, jsonify
import requests
import boto3
import os
import threading
import time

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIG ===
ARCHIVE_ACCESS_KEY = "I5K6xwIfiAKWRAJb"
ARCHIVE_SECRET_KEY = "UbmsVuLSrIYFbVFo"
BOT_TOKEN = "8116523674:AAFVBBfcPvvpYjp0d6OkSpU1cxW1fllECO0"
UPLOAD_ENDPOINT = "https://terabox-archive.onrender.com/upload"  # 🔁 Replace with your actual Render URL

app = Flask(__name__)

# === FLASK ROUTE ===
@app.route('/upload', methods=['POST'])
def upload():
    try:
        terabox_url = request.json.get('url')
        item_name = request.json.get('item_name', 'upload_' + str(int(time.time())))

        # Simulated direct video URL (replace with real extractor)
        direct_url = terabox_url.replace("teraboxlink.com", "teraboxcdn.com") + "/video.mp4"

        response = requests.get(direct_url, stream=True)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch video'}), 400

        s3 = boto3.resource(
            's3',
            endpoint_url='https://s3.us.archive.org',
            aws_access_key_id=ARCHIVE_ACCESS_KEY,
            aws_secret_access_key=ARCHIVE_SECRET_KEY
        )

        bucket = s3.Bucket(item_name)
        bucket.upload_fileobj(response.raw, 'video.mp4')

        archive_link = f"https://archive.org/details/{item_name}"
        return jsonify({'status': 'Upload complete', 'link': archive_link})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === TELEGRAM BOT ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a TeraBox link to upload to Archive.org.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    await update.message.reply_text("⏳ Upload started…")

    payload = {
        "url": link,
        "item_name": "upload_" + str(update.effective_user.id)
    }

    try:
        res = requests.post(UPLOAD_ENDPOINT, json=payload)
        data = res.json()
        if "link" in data:
            await update.message.reply_text(f"✅ Done! Archive link:\n{data['link']}")
        elif "error" in data:
            await update.message.reply_text(f"❌ Upload failed: {data['error']}")
        else:
            await update.message.reply_text("❌ Unknown error occurred.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

# === MAIN ===
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
