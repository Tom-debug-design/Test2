import time
import threading
from discord_webhook import DiscordWebhook
from flask import Flask

webhook_url = "https://discord.com/api/webhooks/your_webhook_here"

app = Flask(__name__)

@app.route("/")
def home():
    return "Atomicbot is alive!"

def send_heartbeat():
    while True:
        try:
            webhook = DiscordWebhook(url=webhook_url, content="🔁 Heartbeat fra Atomicbot")
            webhook.execute()
        except Exception as e:
            print("Feil ved sending:", e)
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=send_heartbeat, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)