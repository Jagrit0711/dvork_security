from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app)

users = []
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
@app.route('/log_sos', methods=['POST'])
def log_sos():
    data = request.get_json()
    timestamp = data.get('timestamp', datetime.now().isoformat())
    # Log the timestamp (you can save it to a file or database)
    print(f"SOS received at {timestamp}")
    return jsonify({"status": "success", "timestamp": timestamp})

@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.json
    users.append(user_data)
    return jsonify({"message": "User added successfully"}), 201

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(users)

@app.route('/log_attendance', methods=['POST'])
def log_attendance():
    card_uid = request.form.get('card_uid')
    print(f"Received card UID: {card_uid}")
    # Add your logic here to handle the card UID
    return jsonify({'status': 'success', 'message': 'Attendance logged'})

def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_server_thread():
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

if __name__ == '__main__':
    start_server_thread()
