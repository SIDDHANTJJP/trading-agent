from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SECRET = os.getenv("SECRET", "xauusd123")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload, timeout=10)

@app.route("/", methods=["GET"])
def home():
    return "XAUUSD Signal Bot Running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data or data.get("secret") != SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    message = f"""
🥇 XAUUSD SIGNAL

Signal: {data.get("signal")}
Entry: {data.get("entry")}
Stoploss: {data.get("stoploss")}
Target 1: {data.get("target1")}
Target 2: {data.get("target2")}
Timeframe: {data.get("timeframe")}
"""
    send_telegram(message)
    return jsonify({"status": "sent"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)