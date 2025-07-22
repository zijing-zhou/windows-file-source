import os
import zipfile
import tarfile
import tempfile
import shutil
from typing import Callable

class DirectoryWalker:
    def __init__(self, root_path: str, callback: Callable[[str, bool, str, str], None]):
        self.root_path = root_path
        self.callback = callback

    def walk(self, archive_name=None, temp_dir=None):
        work_dir = self.root_path if not archive_name else archive_name
        for dirpath, dirnames, filenames in os.walk(work_dir):
            self.callback(dirpath, True, archive_name, temp_dir)
            for dirname in dirnames:
                full_dir_path = os.path.join(dirpath, dirname)
                self.callback(full_dir_path, True, archive_name, temp_dir)
            for filename in filenames:
                full_file_path = os.path.join(dirpath, filename)
                self.callback(full_file_path, False, archive_name, temp_dir)
                
                ext = os.path.splitext(filename)[1].lower()
                if ext == '.wim':
                    self._walk_wim(full_file_path)

    def _walk_wim(self, wim_path):
        import subprocess
        base_dir = os.path.dirname(os.path.abspath(__file__))
        wimlib_exe = os.path.join(base_dir, '..', '..', 'tools', 'wimlib-1.14.4-windows-x86_64-bin', 'wimlib-imagex.exe')

        if not os.path.isfile(wimlib_exe):
            print(f"wimlib-imagex.exe not found at: {wimlib_exe}")
            return
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                subprocess.run([wimlib_exe, 'extract', wim_path, '1', '--dest-dir='+ tmpdir, '--no-acls'], check=True)
                self.walk(wim_path, tmpdir)
            except Exception as e:
                print(f"Failed to extract WIM {wim_path}: {e}")