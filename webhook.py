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

    print("=" * 50)
    print("Webhook Received:")
    print(data)
    print("=" * 50)

    try:

        payment_url = data.get("entity_url")

        print("Payment URL:")
        print(payment_url)

        if payment_url:

            response = requests.get(
                payment_url,
                headers={
                    "Authorization": f"Bearer {API_KEY}"
                }
            )

            print("=" * 50)
            print("Payment Details Status:")
            print(response.status_code)

            print("=" * 50)
            print("Payment Details JSON:")
            print(response.text)

            print("=" * 50)

    except Exception as e:

        print("="
