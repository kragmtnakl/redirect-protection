from flask import Flask, send_file, request
import datetime

app = Flask(__name__)

@app.route("/visit")
def visit():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    now = datetime.datetime.now()

    # سجل بيانات الزيارة في ملف visits.log
    with open("visits.log", "a") as f:
        f.write(f"{now} - {ip} - {user_agent}\n")

    # أرسل صفحة التحويل
    return send_file("visit.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
