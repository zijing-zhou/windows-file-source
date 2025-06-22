from enum_handler import ISORequestHandler
import time

if __name__ == "__main__":
    handler = ISORequestHandler(db_path="iso.db")
    while True:
        handler.process_requests()
        time.sleep(10)
