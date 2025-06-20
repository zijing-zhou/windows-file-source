from downloader.enum_handler import ISORequestHandler

if __name__ == "__main__":
    handler = ISORequestHandler(db_path="iso.db")
    handler.process_requests()
