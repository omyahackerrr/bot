import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
UPI_ID = os.getenv("UPI_ID")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to OMYA GAMING BOT!\nUse /plans to see subscriptions.\nUse /pay for UPI info.\nUse /community to join our groups."
    )

# Command: /plans
async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Subscription Plans:\n"
        "1️⃣ ₹150 – 1 Day Access\n"
        "2️⃣ ₹450 – 1 Week Access\n"
        "3️⃣ ₹800 – 1 Month Access"
    )

# Command: /pay
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📤 UPI Payment Info:\nSend payment to:\n🔗 {UPI_ID}\nThen send screenshot to {ADMIN_USERNAME}"
    )

# Command: /community
async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 Join Our Community:\n"
        "- Telegram: https://t.me/omyahackerrealowner\n"
        "- WhatsApp: https://wa.me/+919112372706\n"
        "- YouTube: https://www.youtube.com/@omyahackerr01\n"
        "- Instagram: https://www.instagram.com/omyahackerr"
    )

# Command: /content (admin only)
async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    if username == ADMIN_USERNAME.replace("@", ""):
        with open("content/sample-wallpaper.jpg", "rb") as photo:
            await update.message.reply_photo(photo, caption="🎮 Your premium gaming wallpaper!")
    else:
        await update.message.reply_text("❌ Only verified users can access premium content.")

# Main app
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plans", plans))
app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("community", community))
app.add_handler(CommandHandler("content", content))

print("✅ Bot is running...")
app.run_polling()
