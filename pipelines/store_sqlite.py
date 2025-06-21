
import sqlite3
import json
from datetime import datetime

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY,
            title TEXT,
            journal TEXT,
            authors TEXT,
            date TEXT,
            abstract TEXT,
            summary TEXT,
            full_text TEXT,
            cluster INTEGER
        );
    """)
    conn.commit()

def insert_data(conn, json_path):
    cur = conn.cursor()
    with open(json_path, "r") as f:
        entries = json.load(f)
    for entry in entries:
        cur.execute("""
            INSERT INTO journal_entries (title, journal, authors, date, abstract, summary, full_text, cluster)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            entry.get("title", ""),
            entry.get("journal", ""),
            ", ".join(entry.get("authors", [])),
            entry.get("date", ""),
            entry.get("abstract", ""),
            entry.get("summary", ""),
            entry.get("full_text", ""),
            entry.get("topic_cluster", -1)
        ))
    conn.commit()

if __name__ == "__main__":
    db_path = "data/agent_data.db"
    json_path = "data/clustered_journal_results_" + datetime.now().strftime('%Y%m%d') + ".json"
    conn = sqlite3.connect(db_path)
    create_tables(conn)
    insert_data(conn, json_path)
    conn.close()
