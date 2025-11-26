from keep_alive import keep_alive
import requests
import time
import pandas as pd
import numpy as np
import datetime

# ============================
# TELEGRAM AYARLARI
# ============================
TELEGRAM_TOKEN = "7953369484:AAFFIYYwpaUwbKqWYKmqmXqaB4c2Yb0vfRs"
CHAT_ID = "1028182811"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram hatası:", e)

# Bot açılış mesajı
send_telegram("🚀 Bot çalıştı! Bitget 15m sinyal botu aktif.")

# ============================
# BITGET 15m MUM VERISI
# ============================
def get_bitget_klines(symbol, interval="15m", limit=200):
    url = "https://api.bitget.com/api/v2/market/history-candles"
    params = {
        "symbol": symbol,
        "granularity": interval,
        "limit": limit
    }
    r = requests.get(url, params=params)
    data = r.json()

    # Veri gelmezse None döndür
    if "data" not in data:
        return None

    df = pd.DataFrame(data["data"])
    df.columns = ["timestamp", "open", "high", "low", "close", "volume"]

    df["timestamp"] = df["timestamp"].astype(int)
    df = df.sort_values("timestamp").reset_index(drop=True)
    df[["open","high","low","close","volume"]] = df[["open","high","low","close","volume"]].astype(float)

    return df

# ============================
# TRADINGVIEW DIRECTION SİNYALİ
# direction: 1 = SELL yönü, -1 = BUY yönü
# ============================
def calculate_direction(df):
    df["dir"] = np.where(df["close"] > df["close"].shift(1), 1, -1)
    df["dir_change"] = df["dir"].diff()
    return df

# ============================
# TAKIP EDILECEK COINLER
# ============================
symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "WLDUSDT",
    "SOLUSDT",
    "SEIUSDT",
    "APTUSDT",
    "SUIUSDT"
]

# ============================
# ANA DÖNGÜ — BOTUN KALBI
# ============================
send_telegram("🔍 Coinler taranıyor...")

while True:
    for coin in symbols:
        df = get_bitget_klines(coin)

        if df is None:
            print("Bitget veri hatası:", coin)
            continue

        df = calculate_direction(df)

        last = df.iloc[-1]

        # BUY sinyali
        if last["dir"] == -1 and last["dir_change"] != 0:
            send_telegram(f"🟢 BUY → {coin} (15m)")

        # SELL sinyali
        if last["dir"] == 1 and last["dir_change"] != 0:
            send_telegram(f"🔴 SELL → {coin} (15m)")

        time.sleep(1)

    time.sleep(5)
