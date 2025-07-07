import os
import win32file
import win32con
import win32api
import win32security
import pywintypes
import datetime

class WindowsFileInfo:
    def __init__(self, filepath: str):
        if not os.path.isfile(filepath):
            self.filestate = False
            return

        self.filepath = filepath
        self.filestate = True
        self.size = None
        self.create_time = None
        self.modify_time = None
        self.access_time = None
        self.is_hidden = False
        self.is_system = False
        self.is_readonly = False
        self.version = None
        self.company = None
        self.owner = None

        self._get_basic_info()
        self._get_file_attributes()
        self._get_version_info()
        self._get_owner()

    def _convert_filetime(self, filetime):
        return datetime.datetime.fromtimestamp(filetime.timestamp())

    def _get_basic_info(self):
        stat = os.stat(self.filepath)
        self.size = stat.st_size
        self.create_time = datetime.datetime.fromtimestamp(stat.st_ctime)
        self.modify_time = datetime.datetime.fromtimestamp(stat.st_mtime)
        self.access_time = datetime.datetime.fromtimestamp(stat.st_atime)

    def _get_file_attributes(self):
        attrs = win32file.GetFileAttributes(self.filepath)
        self.is_hidden = bool(attrs & win32con.FILE_ATTRIBUTE_HIDDEN)
        self.is_system = bool(attrs & win32con.FILE_ATTRIBUTE_SYSTEM)
        self.is_readonly = bool(attrs & win32con.FILE_ATTRIBUTE_READONLY)

    def _get_version_info(self):
        try:
            info = win32api.GetFileVersionInfo(self.filepath, '\\')
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            self.version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"

            lang, codepage = win32api.GetFileVersionInfo(self.filepath, r'\VarFileInfo\Translation')[0]
            str_info = lambda name: win32api.GetFileVersionInfo(
                self.filepath,
                f'\\StringFileInfo\\{lang:04X}{codepage:04X}\\{name}'
            )

            self.company = str_info('CompanyName')
        except Exception as e:
            self.version = None
            self.company = None

    def _get_owner(self):
        try:
            sd = win32security.GetFileSecurity(self.filepath, win32security.OWNER_SECURITY_INFORMATION)
            owner_sid = sd.GetSecurityDescriptorOwner()
            name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
            self.owner = f"{domain}\\{name}"
        except pywintypes.error:
            self.owner = None
