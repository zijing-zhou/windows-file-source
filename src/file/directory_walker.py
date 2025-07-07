import os
from typing import Callable

class DirectoryWalker:
    def __init__(self, root_path: str, callback: Callable[[str, bool], None]):
        self.root_path = root_path
        self.callback = callback

    def walk(self):
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            self.callback(dirpath, is_dir=True)
            for dirname in dirnames:
                full_dir_path = os.path.join(dirpath, dirname)
                self.callback(full_dir_path, is_dir=True)
            for filename in filenames:
                full_file_path = os.path.join(dirpath, filename)
                self.callback(full_file_path, is_dir=False)