from vboxapi import VirtualBoxManager
from vm.vboxshell import createVm
from vm.vboxshell import startVm
from vm.vboxshell import removeVm
from vm.vboxshell import argsToMach
from vm.vboxshell import getMachines
from vm.vboxshell import findDevOfType

class VirtualBox:
    def __init__(self, ctx=None):
        vbox_mgr = VirtualBoxManager() 
        ctx = {
            'global': vbox_mgr,
            'vb': vbox_mgr.getVirtualBox(),
            'const': vbox_mgr.constants,
            '_machlist': None,
            'remote': False,
            'perf': None
        }
        self.ctx = ctx
        self.vbox_mgr = vbox_mgr

    def create_windows_vm(self, name, arch, kind):
        if '_machlist' not in self.ctx:
            self.ctx['_machlist'] = None
        createVm(self.ctx, name, arch, kind)

    def start_windows_vm(self, name):
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            mach = argsToMach(self.ctx, [name, uuid])
            startVm(self.ctx, mach, "gui")

    def poweroff_windows_vm(self, name):
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            mach = argsToMach(self.ctx, [name, uuid])
        pass

    def backup_windows_vm(self, name):
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            mach = argsToMach(self.ctx, [name, uuid])
        pass

    def restore_windows_vm(self, name):
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            mach = argsToMach(self.ctx, [name, uuid])
        pass
        
    def remove_windows_vm(self, name):
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            mach = argsToMach(self.ctx, [name, uuid])
            removeVm(self.ctx, mach)
        
    def create_storage_controller(self, machine):
        try:
            controller_name = "SATA Controller"
            controller = machine.addStorageController(
                controller_name,
                self.ctx['global'].constants.StorageBus_SATA
            )
            
            controller.portCount = 30
            controller.useHostIOCache = True
            
            return {
                'controller': 0,
                'port': 0,      
                'slot': 0       
            }
        except Exception as e:
            return None
    
    def set_vm_resources(self, name, store_path, store_mb,
                         cpu_count: int = 2, memory_gb: int = 4):
        vbox = self.ctx['vb']
        session = self.ctx['global'].getSessionObject(vbox)
        
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            mach = argsToMach(self.ctx, [name, uuid])
        
            lock_result = mach.lockMachine(session, self.ctx['global'].constants.LockType_Write)
            if lock_result != 0:
                return False

            m = session.machine

            hdd = vbox.createMedium("vdi", store_path, 
                                self.ctx['global'].constants.AccessMode_ReadWrite, 
                                self.ctx['global'].constants.DeviceType_HardDisk)
            progress = hdd.createBaseStorage(store_mb * 1024 * 1024, 
                                            [self.ctx['global'].constants.MediumVariant_Standard])
            progress.waitForCompletion(-1)
            if progress.resultCode != 0:
                return False

            controller_name = "SATA"
            try:
                sata_controller = m.addStorageController(controller_name, 
                                                    self.ctx['global'].constants.StorageBus_SATA)
                sata_controller.portCount = 30
                sata_controller.useHostIOCache = True
                
            except Exception as e:
                return False

            m.saveSettings()
            session.unlockMachine()
            return True
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            hdd = vbox.createMedium("vdi", store_path, self.ctx['global'].constants.AccessMode_ReadWrite, 
                                    self.ctx['global'].constants.DeviceType_HardDisk)
            hdd.createBaseStorage(store_mb, (self.ctx['global'].constants.MediumVariant_Standard, ))
            mach = argsToMach(self.ctx, [name, uuid])
            m = mach
            session = self.ctx['global'].getSessionObject(vbox)
            m.lockMachine(session, self.ctx['global'].constants.LockType_Write)
            controller_name = "SATA"
            try:
                sata_controller = m.addStorageController(controller_name, self.ctx['global'].constants.StorageBus_SATA)
                sata_controller.portCount = 30
                sata_controller.useHostIOCache = True
            except Exception as e:
                return False
            hdd = self.ctx['vbox'].createHardDisk("VDI", str(store_path))
            progress = hdd.createBaseStorage(store_mb * 1024 * 1024, [self.ctx['global'].constants.MediumVariant_Standard])
            progress.waitForCompletion(-1)
            try:
                mutable.attachDevice(
                    controller_name,
                    0,              
                    0,              
                    self.ctx['global'].constants.DeviceType_HardDisk,
                    hdd             
                )

                mutable.memorySize = memory_gb * 1024
                mutable.CPUCount = cpu_count
                mutable.saveSettings()
            finally:
                m.session.unlockMachine()
        
    def getUUIDByName(self, name):
        for mach in getMachines(self.ctx, True):
            try:
                if mach.name == name:
                    return mach.id
            except Exception as e:
                return None
        return None

    def getSettingsFilePathByName(self, name):
        for mach in getMachines(self.ctx, True):
            try:
                if mach.name == name:
                    return mach.settingsFilePath
            except Exception as e:
                return None
        return None
