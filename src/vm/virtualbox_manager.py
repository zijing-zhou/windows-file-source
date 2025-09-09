import os
import time
from virtualbox import VirtualBox, Session
from virtualbox.library import LockType, MachineState, StorageBus, DeviceType

class VirtualBoxManager:
    
    def __init__(self):
        self.vbox = VirtualBox()
        self.session = None
    
    def create_windows_vm(self, vm_config):
            self._validate_config(vm_config)
            machine = self._create_machine(vm_config)
            self._configure_hardware(machine, vm_config)
            self._configure_storage(machine, vm_config)
            if vm_config.get('auto_start', True):
                self.start_vm(machine, vm_config.get('start_mode', 'gui'))
            return machine
            
        except Exception as e:
            raise
    
    def _validate_config(self, config):
        required_fields = ['vm_name', 'iso_path']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"{field}")
        
        if not os.path.exists(config['iso_path']):
            raise FileNotFoundError(f"{config['iso_path']}")
    
    def _create_machine(self, config):
        machine = self.vbox.create_machine(
            name=config['vm_name'],
            os_type_id=config.get('os_type', 'Windows10_64'),
            settings_file=config.get('settings_file', ''),
            force_overwrite=config.get('force_overwrite', True)
        )
        
        self.vbox.register_machine(machine)
        return machine
    
    def _configure_hardware(self, machine, config):
        machine.memory_size = config.get('memory_size', 4096)  # MB
        machine.vram_size = config.get('vram_size', 128)      # MB
        machine.cpu_count = config.get('cpu_count', 2)
        machine.bios_settings.IOAPIC_enabled = config.get('enable_ioapic', True)
        if 'hardware' in config:
            self._configure_additional_hardware(machine, config['hardware'])
    
    def _configure_additional_hardware(self, machine, hardware_config):
        pass
    
    def _configure_storage(self, machine, config):
        self.session = Session()
        machine.lock_machine(self.session, LockType.write)
        
        try:
            storage_controller = self.session.machine.add_storage_controller(
                config.get('controller_name', 'SATA Controller'),
                getattr(StorageBus, config.get('storage_bus', 'sata'))
            )

            if config.get('create_hdd', True):
                self._attach_hard_disk(config)

            self._attach_iso(config['iso_path'])

            self.session.machine.save_settings()
            
        finally:
            self.session.unlock_machine()
            self.session = None
    
    def _attach_hard_disk(self, config):
        disk_size = config.get('disk_size', 32) * 1024 * 1024 * 1024  # GB to bytes
        disk_path = os.path.join(
            self.session.machine.settings_file_path,
            config.get('disk_filename', 'disk.vdi')
        )
        
        hdd = self.vbox.create_hard_disk("VDI", disk_path)
        hdd.create_base_storage(disk_size)
        
        self.session.machine.attach_device(
            config.get('controller_name', 'SATA Controller'),
            config.get('hdd_port', 0),
            config.get('hdd_device', 0),
            DeviceType.hard_disk,
            hdd
        )
    
    def _attach_iso(self, iso_path):
        self.session.machine.attach_device(
            "SATA Controller",
            1,
            0,
            DeviceType.dvd,
            iso_path
        )
    
    def start_vm(self, machine, start_mode='gui'):
        print("启动虚拟机...")
        session = Session()
        progress = machine.launch_vm_process(session, start_mode, "")
        progress.wait_for_completion()
        print("虚拟机启动成功！")
    
    def stop_vm(self, machine, save_state=True):
        session = Session()
        machine.lock_machine(session, LockType.shared)
        try:
            if save_state:
                session.console.save_state()
            else:
                session.console.power_down()
        finally:
            session.unlock_machine()
    
    def delete_vm(self, vm_name):
        try:
            machine = self.vbox.find_machine(vm_name)
            machine.remove(delete=True)
        except Exception as e:
            print(f"{str(e)}")
    
    def list_vms(self):
        vms = []
        for machine in self.vbox.machines:
            vms.append({
                'name': machine.name,
                'state': machine.state,
                'os_type': machine.os_type_id
            })
        return vms
    
        return self.vbox.find_machine(vm_name)
