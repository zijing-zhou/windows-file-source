
import sqlite3
import hashlib
from datetime import datetime

class IsoFileProcessor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def calculate_sha1(self, filepath):
        sha1 = hashlib.sha1()
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(65536)  # 64KB chunks
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()

    def process_completed_files(self):
        self.cursor.execute("""
            SELECT id, filename, sourceSHA1 
            FROM iso_file_request 
            WHERE finish_time IS NOT NULL 
            AND state != 'FileReady'
        """)
        
        for row in self.cursor.fetchall():
            file_id, filename, source_sha1 = row
            try:
                current_sha1 = self.calculate_sha1(filename)
                
                if source_sha1 and source_sha1 != current_sha1:
                    continue
                self.cursor.execute("""
                    UPDATE iso_file_request 
                    SET fileSHA1 = ?, state = 'FileReady' 
                    WHERE id = ?
                """, (current_sha1, file_id))
                
                self.conn.commit()
                
            except FileNotFoundError:
                continue
            except Exception as e:
                continue

    def close(self):
        self.conn.close()
