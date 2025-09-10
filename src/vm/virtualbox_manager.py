import os
import subprocess
import time
import shutil
import json

class VirtualBoxManager:
    
    def __init__(self):
        self.vboxmanage_path = self._find_vboxmanage()

    
    def _find_vboxmanage(self):

        if shutil.which("VBoxManage"):
            return "VBoxManage"
        common_paths = [
            r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe",
            r"C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        raise Exception("VBoxManage Error")
    
    def _run_command(self, cmd_args, timeout=60):
        try:
            result = subprocess.run(
                [self.vboxmanage_path] + cmd_args,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='ignore'
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Timeout"
        except Exception as e:
            return False, "", str(e)
    
    def create_windows_vm(self, vm_config):
        vm_name = vm_config['vm_name']

        success, stdout, stderr = self._run_command([
            "createvm", "--name", vm_name, "--register"
        ])
        

        config_commands = [
            ["modifyvm", vm_name, "--ostype", vm_config.get('os_type', 'Windows10_64')],
            ["modifyvm", vm_name, "--memory", str(vm_config.get('memory_size', 4096))],
            ["modifyvm", vm_name, "--vram", str(vm_config.get('vram_size', 128))],
            ["modifyvm", vm_name, "--cpus", str(vm_config.get('cpu_count', 2))],
            ["modifyvm", vm_name, "--ioapic", "on"],
            ["modifyvm", vm_name, "--firmware", "bios"],
            ["modifyvm", vm_name, "--nic1", "nat"],
            ["modifyvm", vm_name, "--audio", "none"],
            ["modifyvm", vm_name, "--usb", "off"]
        ]
        
        for cmd in config_commands:
            self._run_command(cmd)

        disk_path = os.path.join(os.getcwd(), f"{vm_name}.vdi")
        success, stdout, stderr = self._run_command([
            "createhd", 
            "--filename", disk_path, 
            "--size", str(vm_config.get('disk_size', 32768)),
            "--format", "VDI",
            "--variant", "Standard"
        ])
        
        storage_commands = [
            ["storagectl", vm_name, "--name", "SATA", "--add", "sata", "--controller", "IntelAhci"],
            ["storageattach", vm_name, "--storagectl", "SATA", "--port", "0", "--device", "0", 
             "--type", "hdd", "--medium", disk_path]
        ]

        iso_path = vm_config.get('iso_path')
        if iso_path and os.path.exists(iso_path):
            storage_commands.extend([
                ["storagectl", vm_name, "--name", "IDE", "--add", "ide"],
                ["storageattach", vm_name, "--storagectl", "IDE", "--port", "0", "--device", "0", 
                 "--type", "dvddrive", "--medium", iso_path]
            ])
        
        for cmd in storage_commands:
            self._run_command(cmd)
        
        if iso_path:
            self._run_command(["modifyvm", vm_name, "--boot1", "dvd"])
        
        return vm_name
    
    def start_vm(self, vm_name, headless=False):
        mode = "headless" if headless else "gui"
        
        success, stdout, stderr = self._run_command([
            "startvm", vm_name, "--type", mode
        ])

        
        return success
    
    def stop_vm(self, vm_name, force=False):
        if force:
            success, stdout, stderr = self._run_command([
                "controlvm", vm_name, "poweroff"
            ])
        else:
            success, stdout, stderr = self._run_command([
                "controlvm", vm_name, "acpipowerbutton"
            ])
        
        return success
    
    def delete_vm(self, vm_name):
        self.stop_vm(vm_name, force=True)

        success, stdout, stderr = self._run_command([
            "unregistervm", vm_name, "--delete"
        ])

        
        return success
    
    def list_vms(self):
        success, stdout, stderr = self._run_command(["list", "vms"])
        vms = []
        
        if success:
            for line in stdout.splitlines():
                if '"' in line:
                    parts = line.split('"')
                    if len(parts) >= 2:
                        vms.append({
                            'name': parts[1],
                            'uuid': parts[-1].strip(' {}')
                        })
        
        return vms
    
    def get_vm_info(self, vm_name):
        success, stdout, stderr = self._run_command(["showvminfo", vm_name, "--machinereadable"])
        info = {}
        
        if success:
            for line in stdout.splitlines():
                if '=' in line:
                    key, value = line.split('=', 1)
                    info[key] = value.strip('"')
        
        return info

    def create_snapshot(self, vm_name, snapshot_name="initial"):
        success, stdout, stderr = self._run_command([
            "snapshot", vm_name, "take", snapshot_name
        ])
        
        return success