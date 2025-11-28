from flask import Flask, request
import requests

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
    data = request.get_json()

    # 1️⃣ New JSON format from TradingView
    if "Event" in data:
        text = (
            f"⚡ *{data['Event']} Signal Triggered*\n\n"
            f"📌 *Symbol:* {data['Symbol']}\n"
            f"⏱ *Timeframe:* {data['Timeframe']}\n"
            f"💰 *Price:* {data['Price']}"
        )
        send_telegram(text)
        return "ok", 200

    # 2️⃣ Old JSON format: { "message": "..." }
    if "message" in data:
        send_telegram(data["message"])
        return "ok", 200

    # 3️⃣ If nothing matches
    send_telegram("⚠ Received an unsupported JSON format from TradingView.")
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
