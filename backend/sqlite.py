import sqlite3
from config import settings

def get_db():
    conn = sqlite3.connect(settings.DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    print(f"db connection sucessful created")
    return conn
