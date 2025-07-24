from flask import Flask, render_template, request
import datetime
import os

app = Flask(__name__)

@app.route("/visit")
def visit():
    # تسجيل بيانات الزائر
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("visits.log", "a") as f:
        f.write(f"{now} | IP: {ip} | Device: {user_agent}\n")

    # عرض صفحة الحماية
    return render_template("visit.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
