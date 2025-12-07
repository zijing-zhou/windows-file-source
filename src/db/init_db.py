import sqlite3
conn = sqlite3.connect("iso.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS iso_file_request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    type TEXT,
    insert_time DATETIME,
    finish_time DATETIME,
    retry_count INTEGER DEFAULT 0,
    sourceSHA1 TEXT,
    fileSHA1 TEXT,
    state TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS windows_file_info (
    id INTEGER PRIMARY KEY,
    relative_path TEXT,
    file_name TEXT,
    file_size INTEGER,
    sha256 TEXT,
    sha1 TEXT,
    md5 TEXT, 
    version TEXT,
    owner TEXT,
    vendor TEXT,
    isoSHA1 TEXT,
    insert_time DATETIME,
    state TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    access_time DATETIME,
    is_hidden BOOLEAN,
    is_system BOOLEAN,
    is_readonly BOOLEAN,
    is_signed BOOLEAN,
    issuer TEXT,
    thumbprint TEXT,
    signing_time DATETIME,
    file_description TEXT,
    original_filename TEXT,
    internal_name TEXT,
    file_version TEXT,
    product_version TEXT,
    version_number TEXT,
    company_name TEXT,
    legal_copyright TEXT,
    legal_trademarks TEXT,
    product_name TEXT,
    private_build TEXT,
    special_build TEXT,
    operating_system TEXT,
    language TEXT,
    file_type TEXT,
    copyright TEXT,
    Extension TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS vm_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vm_name TEXT NOT NULL UNIQUE,
    generation_time DATETIME,
    iso_id TEXT,
    operating_system TEXT,
    vm_file_name TEXT,
    vm_path TEXT,
    cpu_cores INTEGER,
    memory_mb INTEGER,
    disk_size_gb INTEGER,
    status TEXT,
    host_server TEXT,
    insert_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update_time DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()
