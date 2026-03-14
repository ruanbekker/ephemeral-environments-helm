import sqlite3
import random

DB_FILE = "facts.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT
    )
    """)
    c.execute("SELECT COUNT(*) FROM facts")
    count = c.fetchone()[0]

    if count == 0:
        facts = [
            ("Honey never spoils.",),
            ("Octopus have three hearts.",),
            ("Bananas are berries.",),
            ("A day on Venus is longer than a year on Venus.",),
            ("Sharks existed before trees.",),
            ("Wombats have cube-shaped poop.",)
        ]

        c.executemany("INSERT INTO facts (fact) VALUES (?)", facts)

    conn.commit()
    conn.close()


def get_random_fact():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT fact FROM facts ORDER BY RANDOM() LIMIT 1")
    fact = c.fetchone()[0]
    conn.close()

    return fact

def check_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False
