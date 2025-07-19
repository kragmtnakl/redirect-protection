from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
import os

app = Flask(__name__)

ip_log = {}
blocked_ips = {}
city_block_log = {}
visitor_behavior = []

@app.route('/')
def home():
    return redirect("https://sites.google.com/view/fouadabdoshop")

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    city = data.get('city', 'unknown')
    action = data.get('action', 'unknown')
    stay_time = data.get('stay', 0)
    contacted = data.get('contacted', False)
    now = datetime.now()

    # إزالة الحظر المنتهي
    for ip_banned in list(blocked_ips.keys()):
        if now > blocked_ips[ip_banned]:
            del blocked_ips[ip_banned]
    for city_name in list(city_block_log.keys()):
        if now > city_block_log[city_name]:
            del city_block_log[city_name]

    if city in city_block_log:
        return jsonify({'status': 'blocked_city'}), 403
    if ip in blocked_ips:
        return jsonify({'status': 'blocked_ip'}), 403

    if ip not in ip_log:
        ip_log[ip] = []
    ip_log[ip].append(now)
    recent_clicks = [t for t in ip_log[ip] if now - t < timedelta(minutes=1)]
    ip_log[ip] = recent_clicks

    if len(recent_clicks) >= 2:
        blocked_ips[ip] = now + timedelta(minutes=15)
        return jsonify({'status': 'ip_blocked'}), 403

    if len(recent_clicks) >= 5:
        city_block_log[city] = now + timedelta(minutes=15)

    if not contacted or stay_time < 5:
        visitor_behavior.append(f"مشبوه: {ip} - {user_agent} - {now.strftime('%Y-%m-%d %H:%M:%S')}")

    return jsonify({
        'status': 'ok',
        'ip': ip,
        'city': city,
        'action': action,
        'device': user_agent,
        'time': now.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
