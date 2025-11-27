import _version
import os
import re
import tkinter as tk
from datetime import datetime
from iso.make_iso import ISOBuilder
from myos.windows.make_autounattend import AutoUnattendGenerator
from pathlib import Path
from tkinter import filedialog, simpledialog, messagebox
from vm.virtualbox_manager import VirtualBox

class WindowsFileSource:
    def __init__(self):
        pass

    # Main menu
    def menu(self):
        print("\n1. Download ISO")
        print("2. Analyze ISO")
        print("3. Install Windows Virtual Machine")
        print("4. Analyze VDI File")
        print("5. Import Local ISO")
        print("6. ISO and VMDK file association")
        print("7. Exit")

        # Get the user's input
        choice = input("Please choose an option (1-6): ")

        # Call the corresponding function based on the user's choice
        if choice == "1":
            self.download_iso()
        elif choice == "2":
            self.analyze_iso()
        elif choice == "3":
            self.install_windows_vm()
        elif choice == "4":
            self.analyze_vdi()
        elif choice == "5":
            self.import_local_iso()
        elif choice == "6":
            self.iso_vmdk_association()
        elif choice == "7":
            print("Exiting... Goodbye!")
            return False  # Exit the loop
        else:
            print("Invalid option, please choose again.")
        return True  # Keep the loop running

    # Simulate download ISO operation
    def download_iso(self):
        print("Downloading ISO...")

    # Simulate analyze ISO operation
    def analyze_iso(self):
        print("Analyzing ISO...")

    def ask_number(self, prompt, title, initial):
        while True:
            value = simpledialog.askstring(title, prompt, initialvalue=initial)
            if value is None:
                return None
            if value.isdigit():
                return int(value)
            else:
                messagebox.showerror("Invalid input", "Please enter a valid number!")

    # Simulate install Windows VM operation
    def install_windows_vm(self):
        root = tk.Tk()
        root.withdraw()        
        iso_file_path = filedialog.askopenfilename(
            title="Open ISO File",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")] 
        )
        if iso_file_path:
            cpu_num = self.ask_number("Number of CPU", "Please enter the number:", "4")
            if cpu_num is None:
                return
            memory_num = self.ask_number("Base Memory(GB)", "Please enter the number:", "16")
            if memory_num is None:
                return
            disk_size = self.ask_number("Disk Store(GB)", "Please enter the number:", "100")
            if disk_size is None:
                return
            vbox = VirtualBox()
            vm_name = self.generate_timestamp_name()
            arch = self.get_iso_arch_by_name(iso_file_path)
            version = self.get_windows_version(iso_file_path)
            kind = version + '_' + arch[1:]
            vbox.create_windows_vm(vm_name, arch, kind)
            settingsFilePath = vbox.getSettingsFilePathByName(vm_name)
            file_path = Path(settingsFilePath)
            settingsFileDirectory = file_path.parent
            os.makedirs(settingsFileDirectory / "iso", exist_ok=True)
            generator = AutoUnattendGenerator(
                username="AdminUser",
                password=vm_name,
                hostname=vm_name,
                timezone="China Standard Time",
                kind=kind
            )
            generator.save_to_file(settingsFileDirectory / "iso" / "autounattend.xml")
            output_iso = Path(settingsFileDirectory / "autounattend.iso")
            builder = ISOBuilder()
            builder.write(output_iso, settingsFileDirectory / "iso", vm_name)
            vbox.set_vm_resources(vm_name, memory_gb = memory_num, cpu_count = cpu_num, 
                                  store_mb = 1024*disk_size, store_path = settingsFileDirectory / "store.vdi", 
                                  iso_path = iso_file_path)
            vbox.start_windows_vm(vm_name)
            # Waiting for installation to complete
            # Save VM details to the database
                    
    # Simulate analyze VMDK operation
    def analyze_vdi(self):
        print("Analyzing VMDK file...")
        root = tk.Tk()
        root.withdraw()        
        vdi_file_path = filedialog.askopenfilename(
            title="Open VDI File",
            filetypes=[("VDI files", "*.vdi"), ("All files", "*.*")] 
        )
        if vdi_file_path:
            vbox = VirtualBox()
            vbox.analyze_vdi(vdi_file_path)      

    # Simulate import local ISO operation
    def import_local_iso(self):
        print("Importing local ISO...")
    
    def generate_timestamp_name(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    def get_iso_arch_by_name(self, iso_path):
        filename = os.path.basename(iso_path).lower()
        if any(x in filename for x in ['x64', 'amd64', '64bit', '64-bit']):
            return 'x64'
        elif any(x in filename for x in ['x86', 'i386', '32bit', '32-bit']):
            return 'x86'
        return 'unknown'

    def get_windows_version(self, iso_path: str) -> str:
        try:
            filename = os.path.basename(iso_path).lower()
            
            if any(x in filename for x in ['win11', 'windows11', 'win 11', 'windows 11', 'windows_11']):
                return 'Windows11'
            elif any(x in filename for x in ['win10', 'windows10', 'win 10', 'windows 10', 'windows_10']):
                return 'Windows10'
            elif any(x in filename for x in ['win8', 'windows8', 'win 8', 'windows 8', 'windows_8']):
                return 'Windows8'
            elif any(x in filename for x in ['win7', 'windows7', 'win 7', 'windows 7', 'windows_7']):
                return 'Windows7'
            else:
                return 'Unknown'                
        except Exception as e:
            print(f"Error: {str(e)}")
            return 'Unknown'
    def iso_vmdk_association(self):
        #selete db
        #list vm
        #list iso
        pass
        
# The main loop for interacting with the user
if __name__ == '__main__':
    print("Windows Source File: ",_version.get_version())
    windows_file_source = WindowsFileSource()
    
    # Keep calling the menu until the user chooses to exit
    while True:
        if not windows_file_source.menu():
            break
