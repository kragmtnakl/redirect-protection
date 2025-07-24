from flask import Flask, send_file, request
import datetime
import os

app = Flask(__name__)

@app.route("/visit")
def visit():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    now = datetime.datetime.now()

    with open("visits.log", "a") as f:
        f.write(f"{now} - {ip} - {user_agent}\n")

    return send_file("visit.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
