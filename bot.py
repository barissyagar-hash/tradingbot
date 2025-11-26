from keep_alive import keep_alive
from flask import Flask, request
import requests

# ===============================
# TELEGRAM AYARLARI
# ===============================

TELEGRAM_TOKEN = "7953369484:AAHjWmHHIPQfVZRmlB_EQRtLdVUrkuN22DI"
CHAT_ID = "1021828111"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram hatası:", e)

# ===============================
# FLASK APP
# ===============================

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json

        signal = data.get("signal")
        symbol = data.get("symbol")

        if signal and symbol:
            send_telegram(f"📢 TradingView Sinyali!\n{symbol} → {signal}")
            return {"status": "ok"}, 200

        return {"error": "Eksik veri"}, 400

    except Exception as e:
        return {"error": str(e)}, 500


# ===============================
# KEEP ALIVE
# ===============================

keep_alive()

send_telegram("🚀 Bot aktif! TradingView sinyalleri için webhook dinlemede.")
