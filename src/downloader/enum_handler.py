# downloader/enum_handler.py
import sqlite3
from datetime import datetime
from http_downloader import HTTPDownloader
from magnet_downloader import MagnetDownloader

class ISORequestHandler:
    def __init__(self, db_path='iso.db'):
        self.conn = sqlite3.connect(db_path)
        self.http = HTTPDownloader()
        self.magnet = MagnetDownloader()

    def process_requests(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, url, type, retry_count FROM iso_file_request 
            WHERE finish_time IS NULL AND retry_count < 10
        """)
        rows = cur.fetchall()

        for row in rows:
            id, url, type_, retry = row
            print(f"Processing ID {id} | Type: {type_} | Retry: {retry}")

            try:
                if type_ == 'http':
                    local_filename = self.http.download(url)
                elif type_ in ['magnet', 'magnet:?']:
                    local_filename = self.magnet.download(url)
                else:
                    print(f"Unsupported type: {type_}")
                    continue

                cur.execute("UPDATE iso_file_request SET finish_time=?, retry_count=?, retry_count=?, state = 'Downloaded' WHERE id=?",
                            (datetime.now(), retry + 1, local_filename, id))
            except Exception as e:
                print(f"Error processing ID {id}: {e}")
                cur.execute("UPDATE iso_file_request SET retry_count=? WHERE id=?",
                            (retry + 1, id))

        self.conn.commit()
