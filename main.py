import json
import os
from flask import Flask, request
import requests
from datetime import datetime, time

app = Flask(__name__)

# Завантаження конфігурації
with open("config.json") as f:
    config = json.load(f)

TELEGRAM_TOKEN = config["telegram_token"]
TELEGRAM_CHAT_ID = config["telegram_chat_id"]
WEBHOOK_SECRET = config["webhook_secret"]

allowed_pairs = {"EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"}

TRADING_START = time(8, 0)  # UTC 8:00
TRADING_END = time(17, 0)   # UTC 17:00

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    r = requests.post(url, json=payload)
    return r.status_code, r.text

def is_trading_time():
    now = datetime.utcnow().time()
    return TRADING_START <= now <= TRADING_END

def parse_signal(data):
    pair = data.get("pair")
    if pair not in allowed_pairs:
        return None

    rsi = data.get("RSI", 50)
    if not (rsi < 30 or rsi > 70):
        return None

    if not is_trading_time():
        return None

    pattern = data.get("pattern", "N/A")
    direction = data.get("direction", "N/A")
    timeframe = data.get("timeframe", "N/A")
    sma_signal = data.get("SMA_signal", "N/A")
    entry_price = data.get("entry_price", "N/A")

    text = (
        f"📢 *VIP СИГНАЛ*\n"
        f"📈 Патерн: {pattern}\n"
        f"💹 Пара: {pair}\n"
        f"⏳ Таймфрейм: {timeframe}\n"
        f"✅ Сигнал: {'ВГОРУ' if direction == 'UP' else 'ВНИЗ'}\n"
        f"🔍 RSI: {rsi} {'(перепроданість)' if rsi < 30 else '(перекупленість)'}\n"
        f"📉 Ціна: {'нижче' if sma_signal == 'below' else 'вище'} SMA\n"
        f"📍 Точка входу: {entry_price}"
    )
    return text

@app.route("/webhook", methods=["POST"])
def webhook():
    secret = request.headers.get("X-Webhook-Secret")
    if secret != WEBHOOK_SECRET:
        return {"error": "Unauthorized"}, 401

    data = request.json
    if not data:
        return {"error": "No data"}, 400

    message = parse_signal(data)
    if not message:
        return {"status": "ignored"}, 200

    code, resp = send_telegram_message(message)
    if code == 200:
        return {"status": "sent"}, 200
    else:
        return {"status": "failed", "response": resp}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))