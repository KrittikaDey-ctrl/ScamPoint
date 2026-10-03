from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'scampoint.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS whitelist (domain TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS keywords (word TEXT UNIQUE)''')
    
    whitelist_domains = ['mygov.in', 'police.gov.in', 'rbi.org.in', 'sbi.co.in']
    for domain in whitelist_domains:
        c.execute("INSERT OR IGNORE INTO whitelist (domain) VALUES (?)", (domain,))
        
    scam_keywords = ['digital arrest', 'cbi', 'customs', 'transfer money', 'urgent', 'fedex', 'trai', 'arrest warrant', 'otp']
    for word in scam_keywords:
        c.execute("INSERT OR IGNORE INTO keywords (word) VALUES (?)", (word,))
        
    conn.commit()
    conn.close()

def check_message(text):
    text_lower = text.lower()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("SELECT domain FROM whitelist")
    whitelists = [row[0] for row in c.fetchall()]
    for domain in whitelists:
        if domain in text_lower:
            conn.close()
            return {"status": "safe", "message": f"Message contains verified official domain: {domain}. It appears safe."}
            
    c.execute("SELECT word FROM keywords")
    keywords = [row[0] for row in c.fetchall()]
    detected_words = []
    
    for word in keywords:
        if word in text_lower:
            detected_words.append(word)
            
    conn.close()
    
    if len(detected_words) > 0:
        return {
            "status": "danger",
            "message": "CRITICAL WARNING: Potential Scam Detected",
            "detected": detected_words,
            "law": "STATUTORY FACT: The Ministry of Home Affairs and Indian law do not recognize 'digital arrest'. Authorities will never demand money, isolate you on video calls, or serve arrest notices via messaging platforms."
        }
        
    return {"status": "neutral", "message": "No immediate threat detected, but always remain cautious."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    message = data.get('message', '')
    if not message.strip():
        return jsonify({"status": "error", "message": "Please enter a message to scan."})
    
    result = check_message(message)
    return jsonify(result)

if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        init_db()
    app.run(debug=True, port=5000)