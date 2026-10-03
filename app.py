from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

# Helper function to query the database
def check_threat(message):
    message = message.lower()
    conn = sqlite3.connect('scampoint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT keyword, rebuttal FROM legal_rules")
    rules = cursor.fetchall()
    conn.close()

    triggered_rebuttals = []
    for keyword, rebuttal in rules:
        if keyword in message:
            triggered_rebuttals.append(rebuttal)
            
    return triggered_rebuttals

# Helper function to simulate dispatch (Replace with Twilio API tomorrow)
def dispatch_family_alert(alert_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[URGENT DISPATCH - {timestamp}]")
    print(f"Alert Type: {alert_type}")
    print("Sending SMS to Guardian: 'URGENT: Your elder parent has triggered a ScamPoint Alert. Call them immediately to disrupt a potential scam.'")
    print("--------------------------------------------------\n")
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_message():
    data = request.get_json()
    message = data.get('message', '')
    
    rebuttals = check_threat(message)
    
    if rebuttals:
        # Threat detected! Dispatch silent alert to family.
        dispatch_family_alert("Automated Threat Detection")
        return jsonify({
            "status": "danger",
            "message": "⚠️ Coercive Threat Detected!",
            "rebuttals": rebuttals
        })
    else:
        return jsonify({
            "status": "safe",
            "message": "✅ No known scam keywords detected.",
            "rebuttals": []
        })

@app.route('/sos', methods=['POST'])
def trigger_sos():
    dispatch_family_alert("Manual 1-Tap SOS / Call Panic")
    return jsonify({"status": "success", "message": "SOS Alert dispatched to registered family members."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)