from keep_alive import keep_alive
from flask import Flask, request
import requests
import time
import pandas as pd

# ======================================================
# TELEGRAM AYARLARI
# ======================================================

TELEGRAM_TOKEN = "7953369484:AAFFlYYwpAbWckQwYKmmqxQaB4c2Yb0vFRs"
CHAT_ID = "1021828111"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram hatası:", e)

# ======================================================
# TRADINGVIEW WEBHOOK — SİNYAL ALICI
# ======================================================

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        try:
            data = request.data.decode('utf-8').strip()

            # ÖRN: “BTCUSDT BUY” veya “AVAXUSDT SELL”
            if data:
                send_telegram(f"📢 TradingView Sinyali: {data}")
                print("TradingView sinyali alındı:", data)

            return "OK", 200

        except Exception as e:
            print("Webhook Hatası:", e)
            return "ERROR", 500

    return "Bot is alive!", 200

# ======================================================
# COIN TARAYICI (İstersen kapatabiliriz)
# ======================================================

COIN_LIST = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "AVAXUSDT",
    "DOGEUSDT"
]

def get_price(symbol):
    try:
        url = f"https://api.bitget.com/api/v2/spot/market/tickers?symbol={symbol}"
        data = requests.get(url).json()
        return float(data["data"][0]["lastPr"])
    except:
        return None

def tarama_islemi():
    print("🔍 Coinler taranıyor...")
    for coin in COIN_LIST:
        price = get_price(coin)
        if price:
            print(f"{coin}: {price}")

# ======================================================
# BOTU AKTİF TUT
# ======================================================

keep_alive()

sent_start_message = False

while True:

    if not sent_start_message:
        send_telegram("🚀 Bot aktif! Webhook + Sinyal sistemi açıldı.")
        sent_start_message = True

    # Tarayıcı çalışsın istiyorsan açık kalsın
    tarama_islemi()

    time.sleep(120)
