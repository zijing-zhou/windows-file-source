import xml.etree.ElementTree as ET
from xml.dom import minidom

class AutoUnattendGenerator:
    def __init__(self, username, password, hostname, timezone, language):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.timezone = timezone
        self.language = language
import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime

class AutoUnattendGenerator:
    UNATTEND_NS = "urn:schemas-microsoft-com:unattend"

    def __init__(self, username: str, password: str, hostname: str,
                 timezone: str = "China Standard Time", language: str = "zh-CN"):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.timezone = timezone
        self.language = language
        # validate minimal
        if not all([username, password, hostname]):
            raise ValueError("username, password, hostname error")

    def _add_text_element(self, parent, tag, text):
        el = ET.SubElement(parent, tag)
        el.text = str(text)
        return el

    def _pretty_xml(self, root: ET.Element) -> str:
        rough = ET.tostring(root, encoding="utf-8")
        reparsed = minidom.parseString(rough)
        return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode('utf-8')

    def generate_windows10(self, filename):
        self.render()
        self.write_file(filename)

    def render(self) -> str:
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        ET.register_namespace('', self.UNATTEND_NS)
        ET.register_namespace('wcm', "http://schemas.microsoft.com/WMIConfig/2002/State")
        ET.register_namespace('cpi', "urn:schemas-microsoft-com:cpi")

        # Root element
        unattend = ET.Element(ET.QName(self.UNATTEND_NS, "unattend"))

        settings_wp = ET.SubElement(unattend, "settings", {"pass": "windowsPE"})
        component_wp = ET.SubElement(settings_wp, "component", {
            "name": "Microsoft-Windows-Setup",
            "processorArchitecture": "amd64",
            "publicKeyToken": "31bf3856ad364e35",
            "language": "neutral",
            "versionScope": "nonSxS"
        })
        user_data = ET.SubElement(component_wp, "UserData")
        self._add_text_element(user_data, "AcceptEula", "true")

        settings_spec = ET.SubElement(unattend, "settings", {"pass": "specialize"})
        comp_spec = ET.SubElement(settings_spec, "component", {
            "name": "Microsoft-Windows-Shell-Setup",
            "processorArchitecture": "amd64",
            "publicKeyToken": "31bf3856ad364e35",
            "language": "neutral",
            "versionScope": "nonSxS"
        })
        self._add_text_element(comp_spec, "ComputerName", self.hostname)
        self._add_text_element(comp_spec, "TimeZone", self.timezone)

        settings_oobe = ET.SubElement(unattend, "settings", {"pass": "oobeSystem"})
        comp_oobe = ET.SubElement(settings_oobe, "component", {
            "name": "Microsoft-Windows-Shell-Setup",
            "processorArchitecture": "amd64",
            "publicKeyToken": "31bf3856ad364e35",
            "language": "neutral",
            "versionScope": "nonSxS"
        })

        self._add_text_element(comp_oobe, "RegisteredOwner", self.username)

        autologon = ET.SubElement(comp_oobe, "AutoLogon")
        password_el = ET.SubElement(autologon, "Password")
        self._add_text_element(password_el, "Value", self.password)
        self._add_text_element(password_el, "PlainText", "true")
        self._add_text_element(autologon, "Enabled", "true")
        self._add_text_element(autologon, "Username", self.username)

        oobe = ET.SubElement(comp_oobe, "OOBE")
        self._add_text_element(oobe, "HideEULAPage", "true")
        self._add_text_element(oobe, "HideWirelessSetupInOOBE", "true")
        self._add_text_element(oobe, "NetworkLocation", "Work")
        self._add_text_element(oobe, "ProtectYourPC", "1")

        ua = ET.SubElement(comp_oobe, "UserAccounts")
        local_accounts = ET.SubElement(ua, "LocalAccounts")
        local_account = ET.SubElement(local_accounts, "LocalAccount")
        self._add_text_element(local_account, "Name", self.username)
        self._add_text_element(local_account, "Group", "Administrators")
        pw = ET.SubElement(local_account, "Password")
        self._add_text_element(pw, "Value", self.password)
        self._add_text_element(pw, "PlainText", "true")

        comp_intl = ET.SubElement(settings_oobe, "component", {
            "name": "Microsoft-Windows-International-Core",
            "processorArchitecture": "amd64",
            "publicKeyToken": "31bf3856ad364e35",
            "language": "neutral",
            "versionScope": "nonSxS"
        })
        self._add_text_element(comp_intl, "SystemLocale", self.language)
        self._add_text_element(comp_intl, "UILanguage", self.language)
        self._add_text_element(comp_intl, "UserLocale", self.language)
        self._add_text_element(comp_intl, "InputLocale", self.language)

        settings_audit = ET.SubElement(unattend, "settings", {"pass": "auditSystem"})
        ET.SubElement(settings_audit, "component", {
            "name": "Microsoft-Windows-Deployment",
            "processorArchitecture": "amd64",
            "publicKeyToken": "31bf3856ad364e35",
            "language": "neutral",
            "versionScope": "nonSxS"
        })

        offline_image = ET.SubElement(
            unattend,
            ET.QName("urn:schemas-microsoft-com:cpi", "offlineImage")
        )
        offline_image.set(ET.QName("http://schemas.microsoft.com/WMIConfig/2002/State", "action"), "add")
        offline_image.set(ET.QName("http://schemas.microsoft.com/WMIConfig/2002/State", "source"), "")

        rough = ET.tostring(unattend, encoding="utf-8")
        reparsed = minidom.parseString(rough)
        xml_text = reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
        return "\n".join([line for line in xml_text.splitlines() if line.strip()])

    def write_file(self, path: str = "autounattend.xml"):
        xml_str = self.render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml_str)
        return path


