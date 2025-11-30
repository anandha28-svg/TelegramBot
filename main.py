from flask import Flask, request, jsonify
import requests
import pytz
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = "7930783668:AAEWug4vGEM0aWiRaZ8XT5Xbr_hwdVqMNuQ"
CHAT_ID = "-1003229134855"


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)


@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # Extract fields safely
    event = data.get("Event", "N/A")
    symbol = data.get("Symbol", "N/A")
    timeframe = data.get("Timeframe", "N/A")
    price = data.get("Price", "N/A")
    strategy = data.get("Strategy", "N/A")

    # IST timestamp
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist).strftime("%d-%m-%Y %I:%M:%S %p")

    # Build Telegram message
    text = (
        f"⚡ *{event} Signal Triggered!*\n\n"
        f"📌 *Symbol:* `{symbol}`\n"
        f"⏱ *Timeframe:* `{timeframe}`\n"
        f"💰 *Price:* `{price}`\n"
        f"📒 *Strategy:* `{strategy}`\n"
        f"🕒 *Time (IST):* `{current_time}`\n"
        f"———————————————"
    )

    send_telegram(text)
    return jsonify({"status": "sent"}), 200


@app.route('/ping')
def ping():
    return jsonify({"status": "alive"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
