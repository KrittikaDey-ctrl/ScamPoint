import sqlite3

def setup_database():
    conn = sqlite3.connect('scampoint.db')
    cursor = conn.cursor()
    
    # Create the rules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS legal_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            rebuttal TEXT
        )
    ''')
    
    # Core statutory rebuttals for the hackathon prototype
    rules = [
        ("digital arrest", "FACT: There is no provision for 'Digital Arrest' in Indian Law. Police cannot arrest you over a video call."),
        ("cbi", "FACT: The CBI, Police, or Customs will never demand money transfers or conduct interrogations over Skype or WhatsApp."),
        ("escrow", "FACT: The RBI and law enforcement do not use 'Secret Escrow Accounts' or 'Clearance Accounts' to verify funds."),
        ("aadhaar blocked", "FACT: Your Aadhaar cannot be blocked due to a parcel intercept. This is a standard intimidation tactic."),
        ("fedex", "FACT: Courier companies like FedEx do not transfer calls to the police for illegal parcel claims.")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO legal_rules (keyword, rebuttal) 
        VALUES (?, ?)
    ''', rules)
    
    conn.commit()
    print("Database setup complete. Added legal rules.")
    conn.close()

if __name__ == '__main__':
    setup_database()