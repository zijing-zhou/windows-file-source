import os
import subprocess
import tempfile
import shutil

class WimMountedReader:
    def __init__(self, wim_path, index=1):
        if not self.is_admin():
            raise PermissionError("This script must be run as administrator.")
        if not os.path.isfile(wim_path):
            raise FileNotFoundError(f"WIM file not found: {wim_path}")
        self.wim_path = wim_path
        self.index = index
        self.mount_dir = tempfile.mkdtemp(prefix="wimmount_")
        self.mounted = False

    def mount(self):
        print(f"Mounting WIM image {self.index} to: {self.mount_dir}")
        ps_command = f'''
        Mount-WindowsImage -ImagePath "{self.wim_path}" -Index {self.index} -Path "{self.mount_dir}"
        '''
        result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
        if result.returncode != 0:
            self.cleanup()
            raise RuntimeError(f"Failed to mount WIM image:\n{result.stderr}")
        self.mounted = True

    def list_files(self):
        if not self.mounted:
            self.mount()
        all_files = []
        for root, _, files in os.walk(self.mount_dir):
            for name in files:
                full_path = os.path.join(root, name)
                all_files.append(full_path)
        return all_files

    def unmount(self, commit=False):
        if not self.mounted:
            return
        print(f"Unmounting WIM from: {self.mount_dir}")
        ps_command = f'''
        Dismount-WindowsImage -Path "{self.mount_dir}" -Discard
        '''
        result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to unmount WIM image:\n{result.stderr}")
        self.mounted = False
        self.cleanup()

    def cleanup(self):
        if os.path.exists(self.mount_dir):
            shutil.rmtree(self.mount_dir, ignore_errors=True)

    def __del__(self):
        try:
            self.unmount()
        except Exception:
            self.cleanup()

