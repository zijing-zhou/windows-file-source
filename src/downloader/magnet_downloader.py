# downloader/magnet_downloader.py
import libtorrent as lt
import time
import os

class MagnetDownloader:
    def download(self, magnet_link, save_path='downloads/'):
        os.makedirs(save_path, exist_ok=True)
        ses = lt.session()
        ses.listen_on(6881, 6891)

        params = {
            'save_path': save_path,
            'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        }
        handle = lt.add_magnet_uri(ses, magnet_link, params)

        print("Waiting for metadata...")
        while not handle.has_metadata():
            time.sleep(1)

        print("Downloading...")
        while not handle.is_seed():
            status = handle.status()
            print(f"{status.progress * 100:.2f}% done. Download rate: {status.download_rate / 1000:.2f} kB/s")
            time.sleep(5)

        print("Download completed.")
        return True
