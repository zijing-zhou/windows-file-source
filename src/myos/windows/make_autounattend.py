import xml.etree.ElementTree as ET
from xml.dom import minidom

class AutoUnattendGenerator:
    def __init__(self, username, password, hostname="WindowsPC", timezone="China Standard Time", kind="Windows_10"):
        self.username = username
        self.password = password
        self.computer_name = hostname
        self.timezone = timezone
        
    def _create_element(self, tag, text=None, **attrib):
        element = ET.Element(tag, **attrib)
        if text is not None:
            element.text = text
        return element
    
    def _create_component(self, name, arch="amd64", public_key_token="31bf3856ad364e35", 
                         language="neutral", version_scope="nonSxS"):
        return self._create_element(
            'component',
            name=name,
            processorArchitecture=arch,
            publicKeyToken=public_key_token,
            language=language,
            versionScope=version_scope
        )
    
    def _create_windowsPE_settings(self):
        settings_attrib = {'pass': 'windowsPE'}
        settings = self._create_element('settings', **settings_attrib)

        intl_component = self._create_component("Microsoft-Windows-International-Core-WinPE")
        intl_component.append(self._create_element('InputLocale', 'en-US'))
        intl_component.append(self._create_element('SystemLocale', 'en-US'))
        intl_component.append(self._create_element('UserLocale', 'en-US'))
        intl_component.append(self._create_element('UILanguage', 'zh-CN'))
        settings.append(intl_component)

        setup_component = self._create_component("Microsoft-Windows-Setup")

        disk_config = self._create_element('DiskConfiguration')
        disk_config.append(self._create_element('WillShowUI', 'OnError'))
        
        disk = self._create_element('Disk')
        disk.append(self._create_element('DiskID', '0'))
        disk.append(self._create_element('WillWipeDisk', 'true'))
        
        create_partitions = self._create_element('CreatePartitions')
        create_partition = self._create_element('CreatePartition')
        create_partition.append(self._create_element('Order', '1'))
        create_partition.append(self._create_element('Type', 'Primary'))
        create_partition.append(self._create_element('Extend', 'true'))
        create_partitions.append(create_partition)
        
        disk.append(create_partitions)
        disk_config.append(disk)
        setup_component.append(disk_config)

        user_data = self._create_element('UserData')
        user_data.append(self._create_element('AcceptEula', 'true'))
        setup_component.append(user_data)

        image_install = self._create_element('ImageInstall')
        os_image = self._create_element('OSImage')
        
        install_from = self._create_element('InstallFrom')
        meta_data = self._create_element('MetaData', **{'wcm:action': 'add'})
        meta_data.append(self._create_element('Key', '/IMAGE/INDEX'))
        meta_data.append(self._create_element('Value', '1'))
        install_from.append(meta_data)
        os_image.append(install_from)
        
        install_to = self._create_element('InstallTo')
        install_to.append(self._create_element('DiskID', '0'))
        install_to.append(self._create_element('PartitionID', '1'))
        os_image.append(install_to)
        
        os_image.append(self._create_element('WillShowUI', 'OnError'))
        os_image.append(self._create_element('InstallToAvailablePartition', 'false'))
        image_install.append(os_image)
        setup_component.append(image_install)

        compliance_check = self._create_element('ComplianceCheck')
        compliance_check.append(self._create_element('DisplayReport', 'OnError'))
        setup_component.append(compliance_check)
        
        settings.append(setup_component)
        return settings
    
    def _create_specialize_settings(self):
        settings_attrib = {'pass': 'specialize'}
        settings = self._create_element('settings', **settings_attrib)

        shell_component = self._create_component("Microsoft-Windows-Shell-Setup")
        shell_component.append(self._create_element('ComputerName', self.computer_name))
        settings.append(shell_component)

        deployment_component = self._create_component("Microsoft-Windows-Deployment")
        settings.append(deployment_component)
        
        return settings
    
    def _create_oobeSystem_settings(self):
        settings_attrib = {'pass': 'oobeSystem'}
        settings = self._create_element('settings', **settings_attrib)
        
        shell_component = self._create_component("Microsoft-Windows-Shell-Setup")

        autologon = self._create_element('AutoLogon')
        
        password_elem = self._create_element('Password')
        password_elem.append(self._create_element('Value', self.password))
        password_elem.append(self._create_element('PlainText', 'true'))
        autologon.append(password_elem)
        
        autologon.append(self._create_element('Enabled', 'true'))
        autologon.append(self._create_element('Username', self.username))
        shell_component.append(autologon)

        user_accounts = self._create_element('UserAccounts')

        admin_password = self._create_element('AdministratorPassword')
        admin_password.append(self._create_element('Value', self.password))
        admin_password.append(self._create_element('PlainText', 'true'))
        user_accounts.append(admin_password)

        local_accounts = self._create_element('LocalAccounts')
        local_account_attrib = {'wcm:action': 'add'}
        local_account = self._create_element('LocalAccount', **local_account_attrib)
        local_account.append(self._create_element('Name', self.username))
        local_account.append(self._create_element('DisplayName', self.username))
        local_account.append(self._create_element('Group', 'administrators;users'))
        
        local_password = self._create_element('Password')
        local_password.append(self._create_element('Value', self.password))
        local_password.append(self._create_element('PlainText', 'true'))
        local_account.append(local_password)
        
        local_accounts.append(local_account)
        user_accounts.append(local_accounts)
        shell_component.append(user_accounts)

        visual_effects = self._create_element('VisualEffects')
        visual_effects.append(self._create_element('FontSmoothing', 'ClearType'))
        shell_component.append(visual_effects)

        oobe = self._create_element('OOBE')
        oobe.append(self._create_element('ProtectYourPC', '3'))
        oobe.append(self._create_element('HideEULAPage', 'true'))
        oobe.append(self._create_element('SkipUserOOBE', 'true'))
        oobe.append(self._create_element('SkipMachineOOBE', 'true'))
        oobe.append(self._create_element('NetworkLocation', 'Home'))
        shell_component.append(oobe)

        first_logon_commands = self._create_element('FirstLogonCommands')
        sync_command_attrib = {'wcm:action': 'add'}
        sync_command = self._create_element('SynchronousCommand', **sync_command_attrib)
        sync_command.append(self._create_element('Order', '2'))
        sync_command.append(self._create_element('Description', 'Shutdown after installation'))
        sync_command.append(self._create_element('CommandLine', 'cmd.exe /c shutdown /s /f /t 0'))
        first_logon_commands.append(sync_command)
        shell_component.append(first_logon_commands)

        shell_component.append(self._create_element('TimeZone', self.timezone))
        
        settings.append(shell_component)
        return settings
    
    def generate_xml(self):
        root = ET.Element('unattend')
        root.set('xmlns', 'urn:schemas-microsoft-com:unattend')
        root.set('xmlns:wcm', 'http://schemas.microsoft.com/WMIConfig/2002/State')
        root.append(self._create_windowsPE_settings())
        root.append(self._create_specialize_settings())
        root.append(self._create_oobeSystem_settings())
        rough_string = ET.tostring(root, encoding='utf-8')

        from xml.dom import minidom
        try:
            parsed = minidom.parseString(rough_string)
            return parsed.toprettyxml(indent="    ", encoding="utf-8").decode('utf-8')
        except Exception as e:
            return self._simple_pretty_xml(rough_string.decode('utf-8'))
    
    def _simple_pretty_xml(self, xml_string):
        import re
        xml_string = re.sub(r'>\s*<', '>\n<', xml_string)
        lines = xml_string.split('\n')
        
        indent_level = 0
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('</'):
                indent_level -= 1
                
            formatted_lines.append(' ' * (indent_level * 4) + line)
            
            if line.startswith('<') and not line.startswith('</') and not line.endswith('/>'):
                indent_level += 1
                
        return '<?xml version="1.0" encoding="utf-8"?>\n' + '\n'.join(formatted_lines)
    
    def save_to_file(self, filename):
        xml_content = self.generate_xml()
        
        from pathlib import Path
        file_path = Path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
