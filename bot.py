from keep_alive import keep_alive
from flask import Flask, request
import requests
import json

# ===============================
# TELEGRAM AYARLARI
# ===============================

TELEGRAM_TOKEN = "7953369484:AAHQRGl0O-np81FujOn3VDh562uyKMx5D3I"
CHAT_ID = "1021828111"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram hatası:", e)

# ===============================
# FLASK → TRADINGVIEW WEBHOOK
# ===============================

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # TradingView senin gönderdiğin JSON'u buraya yollayacak
    signal = data.get("signal")
    symbol = data.get("symbol")

    if signal and symbol:
        send_telegram(f"📢 TradingView Sinyali!\n\n{symbol} → {signal}")

    return {"status": "ok"}, 200


# ===============================
# KEEP ALIVE
# ===============================

keep_alive()

# Bot açıldığında 1 kere mesaj
send_telegram("🚀 Bot aktif! TradingView sinyalleri için webhook hazır. /webhook dinlemede.")
