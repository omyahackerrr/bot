import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8116523674:AAFVBBfcPvvpYjp0d6OkSpU1cxW1fllECO0"
UPLOAD_ENDPOINT = "https://your-render-url.onrender.com/upload"  # Replace with your actual Render URL

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
        else:
            await update.message.reply_text("❌ Upload failed.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
