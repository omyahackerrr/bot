require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

const plans = `
💰 *Subscription Plans*:
1️⃣ ₹150 – 1 Day Access  
2️⃣ ₹450 – 1 Week Access  
3️⃣ ₹800 – 1 Month Access
`;

const communityLinks = `
🔗 *Join Our Community*:
- [Telegram Channel](https://t.me/omyahackerrealowner)
- [WhatsApp](https://wa.me/+919112372706)
- [YouTube](https://www.youtube.com/@omyahackerr01)
- [Instagram](https://www.instagram.com/omyahackerr)
`;

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, `👋 Welcome to *OMYA GAMING BOT*!\nUse /plans to see subscriptions.\nUse /pay to get UPI info.\nUse /community to join our groups.`, { parse_mode: 'Markdown' });
});

bot.onText(/\/plans/, (msg) => {
  bot.sendMessage(msg.chat.id, plans, { parse_mode: 'Markdown' });
});

bot.onText(/\/pay/, (msg) => {
  bot.sendMessage(msg.chat.id, `📤 *UPI Payment Info*\nSend payment to:\n*${process.env.UPI_ID}*\nThen send screenshot to ${process.env.ADMIN_USERNAME}`, { parse_mode: 'Markdown' });
});

bot.onText(/\/community/, (msg) => {
  bot.sendMessage(msg.chat.id, communityLinks, { parse_mode: 'Markdown' });
});

bot.onText(/\/content/, (msg) => {
  if (msg.from.username === process.env.ADMIN_USERNAME.replace('@', '')) {
    bot.sendPhoto(msg.chat.id, fs.readFileSync('./content/sample-wallpaper.jpg'), {
      caption: '🎮 Your premium gaming wallpaper!'
    });
  } else {
    bot.sendMessage(msg.chat.id, '❌ Only verified users can access premium content.');
  }
});
