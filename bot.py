import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_download_link(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        download_button = soup.find('a', {'class': 'download-link'})
        if download_button:
            return download_button['href']
        else:
            return None
    except Exception as e:
        print("Error fetching download link:", e)
        return None

def search_vegamovies(movie_name):
    search_url = f"https://vegamovies.cy/search/{movie_name.replace(' ', '-')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_movie = soup.find('a', {'class': 'movie-title'})
    if first_movie:
        return first_movie['href']
    return None

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello! मुझे Vegamovies का movie name या link भेजो, मैं video link fetch कर दूँगा।"
    )

def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text

    if user_input.startswith("http"):
        url = user_input
    else:
        url = search_vegamovies(user_input)

    download_link = get_download_link(url)

    if download_link:
        update.message.reply_text(f"✅ Video Download Link:\n{download_link}")
    else:
        update.message.reply_text("❌ मुझे download link नहीं मिला। कृपया सही लिंक भेजें।")

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
