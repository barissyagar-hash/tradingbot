from keep_alive import keep_alive
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime

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
# TARANACAK COIN LİSTESİ
# ======================================================

COIN_LIST = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "AVAXUSDT",
    "DOGEUSDT"
]

# ======================================================
# FİYAT ÇEKEN FONKSİYON (BİTGET REAL API)
# ======================================================

def get_price(symbol):
    try:
        url = f"https://api.bitget.com/api/v2/spot/market/tickers?symbol={symbol}"
        data = requests.get(url).json()

        price = float(data["data"][0]["lastPr"])
        return price

    except Exception as e:
        print("Fiyat çekme hatası:", e)
        return None

# ======================================================
# TARAYICI
# ======================================================

def tarama_islemi():
    print("🔍 Coinler taranıyor...")

    for coin in COIN_LIST:
        price = get_price(coin)

        if price is None:
            continue

        print(f"{coin} fiyat: {price}")

        # Basit sinyal örneği
        if price > 100:
            send_telegram(f"📈 AL SİNYALİ! {coin} fiyat: {price}")

# ======================================================
# ANA DÖNGÜ
# ======================================================

keep_alive()

sent_start_message = False

while True:

    if not sent_start_message:
        send_telegram("🚀 Bot çalıştı! Bitget sinyal botu aktif.")
        sent_start_message = True

    tarama_islemi()

    time.sleep(120)
