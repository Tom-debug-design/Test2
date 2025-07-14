from flask import Flask, request, jsonify
import os
import time
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/...")  # Sett default hvis ønskelig

@app.route('/')
def index():
    return 'Atomicbot heartbeat server is running!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return jsonify({"message": "Webhook endpoint is alive. Send a POST request to trigger Discord."}), 200

    if request.method == 'POST':
        payload = request.json or {}
        message = payload.get("message", "Default test message from Atomicbot.")

        try:
            data = {"content": f"📡 Heartbeat: {message} — {time.strftime('%Y-%m-%d %H:%M:%S')}"}
            response = requests.post(DISCORD_WEBHOOK_URL, json=data)

            if response.status_code == 204:
                return jsonify({"status": "ok", "detail": "Message sent to Discord"}), 200
            else:
                return jsonify({"status": "error", "code": response.status_code, "response": response.text}), 500
        except Exception as e:
            return jsonify({"status": "exception", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)