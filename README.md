# TeraBox to Archive.org Uploader

## 🔧 Setup

1. Create a new Web Service on [Render](https://render.com)
2. Upload all files or connect GitHub
3. Set these environment variables:
   - ARCHIVE_ACCESS_KEY = I5K6xwIfiAKWRAJb
   - ARCHIVE_SECRET_KEY = UbmsVuLSrIYFbVFo
   - TELEGRAM_BOT_TOKEN = 8116523674:AAFVBBfcPvvpYjp0d6OkSpU1cxW1fllECO0
4. Deploy and go live

## 📲 Telegram Bot

- Send TeraBox link to bot
- Bot replies with upload progress and final Archive.org link

## 🔗 Archive.org

- Videos are uploaded using S3-compatible API
- Final link format: https://archive.org/details/{item_name}
