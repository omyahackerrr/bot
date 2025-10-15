from flask import Flask, request, redirect
import os
from db import save_user
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

FRONTEND_URL = os.getenv("FRONTEND_URL")

@app.route('/verify', methods=['GET'])
def verify():
    telegram_id = request.args.get('id')
    if telegram_id:
        save_user(telegram_id)
        return redirect(f"{FRONTEND_URL}?verified=true")
    return "Missing Telegram ID", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
