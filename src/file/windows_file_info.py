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
        self.file_description = None
        self.original_filename = None
        self.internal_name = None
        self.file_version = None
        self.product_version = None
        self.version_number = None
        self.company_name = None
        self.legal_copyright = None
        self.legal_trademarks = None
        self.product_name = None
        self.private_build = None
        self.special_build = None
        self.operating_system = None
        self.language = None
        self.type = None
        self.copyright = None

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

            translations = win32api.GetFileVersionInfo(self.filepath, r'\VarFileInfo\Translation')
            if translations:
                lang, codepage = translations[0]
                str_info_path = f'\\StringFileInfo\\{lang:04X}{codepage:04X}\\'
                
                def get_str_info(name):
                    try:
                        return win32api.GetFileVersionInfo(self.filepath, str_info_path + name)
                    except:
                        return None
                
                # 获取所有版本信息字段
                self.file_description = get_str_info('FileDescription')
                self.original_filename = get_str_info('OriginalFilename')
                self.internal_name = get_str_info('InternalName')
                self.file_version = get_str_info('FileVersion')
                self.product_version = get_str_info('ProductVersion')
                self.version_number = self.version  # 使用已解析的版本号
                self.company_name = get_str_info('CompanyName')
                self.legal_copyright = get_str_info('LegalCopyright')
                self.legal_trademarks = get_str_info('LegalTrademarks')
                self.product_name = get_str_info('ProductName')
                self.private_build = get_str_info('PrivateBuild')
                self.special_build = get_str_info('SpecialBuild')
                self.operating_system = get_str_info('OperatingSystem')
                self.language = get_str_info('Language')
                self.type = get_str_info('Type')
                self.copyright = get_str_info('Copyright')
                
                # 保持向后兼容
                self.company = self.company_name
                
        except Exception as e:
            # 保持原有错误处理
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