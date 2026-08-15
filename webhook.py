from flask import Flask

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    return "OK", 200


if __name__ == "__main__":
    app.run()
