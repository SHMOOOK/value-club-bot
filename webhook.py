import os
import requests

from flask import Flask
from flask import request

app = Flask(__name__)

API_KEY = os.getenv("STREAMPAY_API_KEY")


@app.route("/")
def home():
    return "Value Club Webhook Running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    print("Webhook Received:")
    print(data)

    try:

        payment_url = data.get("entity_url")

        if payment_url:

            response = requests.get(
                payment_url,
                headers={
                    "Authorization": f"Bearer {API_KEY}"
                }
            )

            print("Payment Details:")
            print(response.json())

    except Exception as e:

        print("ERROR:")
        print(str(e))

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
