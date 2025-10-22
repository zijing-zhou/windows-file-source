import subprocess
import os

class ISOBuilder:
    def __init__(self):
        pass

    def write(self, iso_dest_path, file_src_path, iso_name):
        #ISOCreate -vl XXX .\XXX.iso .\XXX\ -q        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ISOCreate = os.path.join(base_dir, '..', '..', 'tools', 'ISOCreate', 'ISOCreate.exe')

        if not os.path.isfile(ISOCreate):
            print(f"ISOCreate.exe not found at: {ISOCreate}")
            return
        try:
            subprocess.run([ISOCreate, '-vl', iso_name, iso_dest_path, file_src_path, '-q'], check=True)
        except Exception as e:
            print(f"Failed to create iso: {e}")
