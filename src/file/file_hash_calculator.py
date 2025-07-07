import hashlib
import os

class FileHashCalculator:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filestate = True
        self.md5 = None
        self.sha1 = None
        self.sha256 = None

        if os.path.isfile(filepath):
            self._calculate_hashes()
        else:
            self.filestate = False

    def _calculate_hashes(self, chunk_size=8192):
        hash_md5 = hashlib.md5()
        hash_sha1 = hashlib.sha1()
        hash_sha256 = hashlib.sha256()

        with open(self.filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                hash_md5.update(chunk)
                hash_sha1.update(chunk)
                hash_sha256.update(chunk)

        self.md5 = hash_md5.hexdigest()
        self.sha1 = hash_sha1.hexdigest()
        self.sha256 = hash_sha256.hexdigest()

