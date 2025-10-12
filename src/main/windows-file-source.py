import os
import re
import _version
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from vm.virtualbox_manager import VirtualBox

class WindowsFileSource:
    def __init__(self):
        pass

    # Main menu
    def menu(self):
        print("\n1. Download ISO")
        print("2. Analyze ISO")
        print("3. Install Windows Virtual Machine")
        print("4. Analyze VMDK File")
        print("5. Import Local ISO")
        print("6. Exit")

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
            self.analyze_vmdk()
        elif choice == "5":
            self.import_local_iso()
        elif choice == "6":
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

    # Simulate install Windows VM operation
    def install_windows_vm(self):
        root = tk.Tk()
        root.withdraw()        
        file_path = filedialog.askopenfilename(
            title="Open ISO File",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")] 
        )        
        if file_path:
            vbox = VirtualBox()
            vm_name = self.generate_timestamp_name()
            arch = self.get_iso_arch_by_name(file_path)
            version = self.get_windows_version(file_path)
            kind = version + '_' + arch[1:]
            vbox.create_windows_vm(vm_name, arch, kind)
            vbox.set_vm_memory(vm_name, 32)
            #todo set iso and vdi
            vbox.create_complete_sata_setup(vm_name=vm_name, iso_path=file_path, hdd_path)
            vbox.start_vm(vm_name)
            print("Install ...")
            # wait install finish
            vbox.start_shutdown(vm_name)
            # save info to db
                    
    # Simulate analyze VMDK operation
    def analyze_vmdk(self):
        print("Analyzing VMDK file...")

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
        
# The main loop for interacting with the user
if __name__ == '__main__':
    print("Windows Source File: ",_version.get_version())
    windows_file_source = WindowsFileSource()
    
    # Keep calling the menu until the user chooses to exit
    while True:
        if not windows_file_source.menu():
            break
