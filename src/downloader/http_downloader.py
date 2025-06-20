# downloader/http_downloader.py
import requests
import os

class HTTPDownloader:
    def download(self, url, save_path='downloads/'):
        os.makedirs(save_path, exist_ok=True)
        local_filename = os.path.join(save_path, url.split('/')[-1])
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
