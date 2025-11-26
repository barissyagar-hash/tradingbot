from keep_alive import keep_alive
import requests
import time
import numpy as np

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
    except Exception:
        pass

# ===============================
# TARANACAK COIN LİSTESİ
# ===============================

COINS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "AVAXUSDT",
    "XRPUSDT",
    "DOGEUSDT"
]

# ===============================
# BİTGET FİYAT ÇEKME
# ===============================

def get_price(symbol):
    try:
        url = f"https://api.bitget.com/api/v2/spot/market/tickers?symbol={symbol}"
        data = requests.get(url).json()
        return float(data["data"][0]["lastPr"])
    except:
        return None

# ===============================
# ZIGZAG ALGORTİMA (Dip / Tepe)
# ===============================
# BY-Trader mantığı → 
# Dip = Buy, Tepe = Sell

DEPTH = 5   # ZigZag hassasiyeti
DEV = 0.3   # Fiyat sapma yüzdesi

last_buy = {}
last_sell = {}

def zigzag(prices):
    if len(prices) < DEPTH * 2:
        return None

    window = prices[-DEPTH:]
    prev_window = prices[-DEPTH*2:-DEPTH]

    min_now = min(window)
    max_now = max(window)

    min_prev = min(prev_window)
    max_prev = max(prev_window)

    # DIP = BUY
    if min_now < min_prev and (min_prev - min_now) / min_prev > DEV/100:
        return "BUY"

    # TOP = SELL
    if max_now > max_prev and (max_now - max_prev) / max_prev > DEV/100:
        return "SELL"

    return None

# ===============================
# ANA TARAYICI
# ===============================

def scan():
    global last_buy, last_sell

    for coin in COINS:
        history = []

        # son 15 fiyatı çek
        for _ in range(15):
            p = get_price(coin)
            if p:
                history.append(p)
            time.sleep(0.2)

        if len(history) < 10:
            continue

        signal = zigzag(history)

        if signal == "BUY":
            if last_buy.get(coin) != p:
                send_telegram(f"🟢 BUY sinyali → {coin}\nFiyat: {history[-1]}")
                last_buy[coin] = p

        if signal == "SELL":
            if last_sell.get(coin) != p:
                send_telegram(f"🔴 SELL sinyali → {coin}\nFiyat: {history[-1]}")
                last_sell[coin] = p


# ===============================
# KEEP ALIVE + ANA DÖNGÜ
# ===============================

keep_alive()
send_telegram("🚀 BY-Trader ZigZag Bot aktif! TradingView gerekmiyor.")

while True:
    scan()
    time.sleep(20)
