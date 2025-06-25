
import sqlite3
from datetime import datetime

def insert_download_request(url: str, type: str, db_path: str = 'iso.db'):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO iso_file_request 
            (url, type, insert_time, finish_time, retry_count, state)
            VALUES (?, ?, ?, NULL, 0, 'NewFile')
        ''', (url, type, current_time))
        conn.commit()
        print(f"New File OK")
    except sqlite3.Error as e:
        print(f"Database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("help: python insert_download_request.py <URL> <type>")
        print("type:http or magnet")
        sys.exit(1)
    
    url = sys.argv[1]
    type = sys.argv[2].lower()
    
    if type not in ('http', 'magnet'):
        print("Error: type must is http or magnet")
        sys.exit(1)
    
    insert_download_request(url, type)
