import sqlite3
conn = sqlite3.connect("iso.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS iso_file_request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    type TEXT,
    insert_time DATETIME,
    finish_time DATETIME,
    retry_count INTEGER DEFAULT 0,
    sourceSHA1 TEXT,
    fileSHA1 TEXT,
    state TEXT
)
""")
conn.commit()
conn.close()
