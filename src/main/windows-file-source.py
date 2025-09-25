import tkinter as tk
from main import _version
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
        print("Installing Windows Virtual Machine...")
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Open ISO File",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")] 
        )
        if file_path:
            pass
        else:
            return
        vbox = VirtualBox()
        vbox.create_windows_vm("Win10-VM", "x64", "Windows10_64")
        
    # Simulate analyze VMDK operation
    def analyze_vmdk(self):
        print("Analyzing VMDK file...")

    # Simulate import local ISO operation
    def import_local_iso(self):
        print("Importing local ISO...")

# The main loop for interacting with the user
if __name__ == '__main__':
    print("Windows Source File: ",_version.get_version())
    windows_file_source = WindowsFileSource()
    
    # Keep calling the menu until the user chooses to exit
    while True:
        if not windows_file_source.menu():
            break
