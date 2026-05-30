from flask import Flask, request, jsonify
import os, requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, data=data, timeout=10)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data.get("secret") != SECRET_KEY:
        return jsonify({"error": "unauthorized"}), 401

    msg = f"""
📢 <b>Trading Signal</b>

Symbol: {data.get('symbol')}
Signal: {data.get('signal')}
Entry: {data.get('entry')}
Target 1: {data.get('target1')}
Target 2: {data.get('target2')}
Stoploss: {data.get('stoploss')}
Timeframe: {data.get('timeframe')}

⚠️ Paper trade first. Not financial advice.
"""
    send_telegram(msg)
    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(port=5000)