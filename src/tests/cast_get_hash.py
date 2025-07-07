import sqlite3
import os
from datetime import datetime

from src.file.directory_walker import DirectoryWalker
from src.file.file_hash_calculator import FileHashCalculator
from src.file.file_signature_info import FileSignatureInfo
from src.file.windows_file_info import WindowsFileInfo
def print_callback(path, is_dir):
    type_str = "Directory" if is_dir else "File"
    print(f"{type_str}: {path}")
    if not is_dir:
        fileInfo = WindowsFileInfo( path )
        fileHash = FileHashCalculator( path )
        fileSignature = FileSignatureInfo( path )
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO windows_file_info (
                relative_path, file_name, file_size,
                sha256, sha1, md5,
                version, owner, vendor, isoSHA1,
                insert_time, state,
                create_time, modify_time, access_time,
                is_hidden, is_system, is_readonly,
                is_signed, issuer, thumbprint, signing_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                path[2:], os.path.basename(path), fileInfo.size,
                fileHash.sha256, fileHash.sha1, fileHash.md5,
                fileInfo.version, fileInfo.owner, fileInfo.company, "",
                datetime.now(), "ok",
                fileInfo.create_time, fileInfo.modify_time, fileInfo.access_time,
                fileInfo.is_hidden, fileInfo.is_system, fileInfo.is_readonly,
                fileSignature.is_signed, fileSignature.issuer, fileSignature.thumbprint, fileSignature.signing_time
            ))
        conn.commit()
conn = sqlite3.connect("iso.db")
walker = DirectoryWalker("G:\\", print_callback)
walker.walk()
conn.commit()
conn.close()
