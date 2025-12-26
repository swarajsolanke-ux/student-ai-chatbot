import sqlite3
from config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    print(f"db connection sucessful created")
    return conn
