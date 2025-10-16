import xml.etree.ElementTree as ET
from xml.dom import minidom

class AutoUnattendGenerator:
    def __init__(self, username, password, hostname, timezone, language):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.timezone = timezone
        self.language = language

    def prettify(self, elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding="utf-8")

    def generate(self, output_file="autounattend.xml"):
        root = ET.Element("unattend", xmlns="urn:schemas-microsoft-com:unattend")

        settings_pe = ET.SubElement(root, "settings", pass="windowsPE")

        comp_pe = ET.SubElement(settings_pe, "component", name="Microsoft-Windows-International-Core-WinPE", processorArchitecture="amd64", publicKeyToken="31bf3856ad364e35", language="neutral", versionScope="nonSxS")
        ET.SubElement(comp_pe, "InputLocale").text = self.language
        ET.SubElement(comp_pe, "SystemLocale").text = self.language
        ET.SubElement(comp_pe, "UILanguage").text = self.language
        ET.SubElement(comp_pe, "UILanguageFallback").text = self.language
        ET.SubElement(comp_pe, "UserLocale").text = self.language

        comp_disk = ET.SubElement(settings_pe, "component", name="Microsoft-Windows-Setup", processorArchitecture="amd64", publicKeyToken="31bf3856ad364e35", language="neutral", versionScope="nonSxS")
        ET.SubElement(comp_disk, "ImageInstall").append(
            ET.Element("OSImage", attrib={"InstallFrom": "", "InstallTo": ""})
        )

        image_install = ET.SubElement(comp_disk, "ImageInstall")
        os_image = ET.SubElement(image_install, "OSImage")
        install_to = ET.SubElement(os_image, "InstallTo")
        ET.SubElement(install_to, "DiskID").text = "0"
        ET.SubElement(install_to, "PartitionID").text = "1"
        ET.SubElement(os_image, "InstallToAvailablePartition").text = "true"

        ET.SubElement(comp_disk, "UserData").append(ET.Element("AcceptEula", text="true"))

        settings_spec = ET.SubElement(root, "settings", pass="specialize")
        comp_spec = ET.SubElement(settings_spec, "component", name="Microsoft-Windows-Shell-Setup", processorArchitecture="amd64", publicKeyToken="31bf3856ad364e35", language="neutral", versionScope="nonSxS")
        ET.SubElement(comp_spec, "ComputerName").text = self.hostname
        ET.SubElement(comp_spec, "TimeZone").text = self.timezone

        settings_oobe = ET.SubElement(root, "settings", pass="oobeSystem")
        comp_oobe = ET.SubElement(settings_oobe, "component", name="Microsoft-Windows-Shell-Setup", processorArchitecture="amd64", publicKeyToken="31bf3856ad364e35", language="neutral", versionScope="nonSxS")

        user_accounts = ET.SubElement(comp_oobe, "UserAccounts")
        local_accounts = ET.SubElement(user_accounts, "LocalAccounts")
        local_account = ET.SubElement(local_accounts, "LocalAccount", wcm__action="add")
        ET.SubElement(local_account, "Name").text = self.username
        ET.SubElement(local_account, "Group").text = "Administrators"
        ET.SubElement(local_account, "Password").append(
            ET.Element("Value", text=self.password)
        )

        oobe = ET.SubElement(comp_oobe, "OOBE")
        ET.SubElement(oobe, "HideEULAPage").text = "true"
        ET.SubElement(oobe, "HideWirelessSetupInOOBE").text = "true"
        ET.SubElement(oobe, "NetworkLocation").tex
