import sqlite3
import json

DB_NAME = "soc_logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_ip TEXT,
            event_type TEXT,
            message TEXT,
            risk TEXT,
            score REAL,
            attack_type TEXT,
            full_log TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_log(log_entry):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (
            timestamp, source_ip, event_type, message,
            risk, score, attack_type, full_log
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        log_entry["timestamp"],
        log_entry["source_ip"],
        log_entry["event_type"],
        log_entry["message"],
        log_entry["ai_analysis"]["risk"],
        log_entry["ai_analysis"]["score"],
        log_entry["ai_analysis"]["attack_type"],
        json.dumps(log_entry)
    ))

    conn.commit()
    conn.close()


def get_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, source_ip, event_type, message, risk, score, attack_type
        FROM logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    logs = []

    for row in rows:
        logs.append({
            "id": row[0],
            "timestamp": row[1],
            "source_ip": row[2],
            "event_type": row[3],
            "message": row[4],
            "ai_analysis": {
                "risk": row[5],
                "score": row[6],
                "attack_type": row[7]
            }
        })

    return logs