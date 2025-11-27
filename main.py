from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "7930783668:AAEWug4vGEM0aWiRaZ8XT5Xbr_hwdVqMNuQ"
CHAT_ID = "8349018045"

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()

    message = data.get("message", "No message received from TradingView")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    requests.post(url, data=payload)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)