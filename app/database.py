import sqlite3
from datetime import datetime

DB_PATH = "jailbreaklab.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            prompt TEXT,
            score INTEGER,
            risk_level TEXT,
            triggered_rules TEXT,
            decision TEXT,
            message TEXT,
            ia_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_record(result, ia_response=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registros
        (fecha, prompt, score, risk_level, triggered_rules, decision, message, ia_response)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        result.prompt,
        result.score,
        result.risk_level,
        ", ".join(result.triggered_rules),
        result.decision,
        result.message,
        ia_response
    ))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros ORDER BY fecha DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
