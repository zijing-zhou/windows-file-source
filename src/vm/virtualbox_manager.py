from vboxapi import VirtualBoxManager
from vm.vboxshell import createVm
from vm.vboxshell import startVm
from vm.vboxshell import removeVm
from vm.vboxshell import argsToMach
from vm.vboxshell import getMachines
from vm.vboxshell import findDevOfType
from pathlib import Path
import time
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

    def create_windows_vm(self, mach_name, arch, kind):
        if '_machlist' not in self.ctx:
            self.ctx['_machlist'] = None
        createVm(self.ctx, mach_name, arch, kind)

    def start_windows_vm(self, mach_name):
        mach_uuid = self.getUUIDByName(mach_name)
        if mach_uuid is not None:
            mach_mach = argsToMach(self.ctx, [mach_name, mach_uuid])
            startVm(self.ctx, mach_mach, "gui")

    def poweroff_windows_vm(self, mach_name):
        mach_uuid = self.getUUIDByName(mach_name)
        if mach_uuid is not None:
            mach_mach = argsToMach(self.ctx, [mach_name, mach_uuid])
        pass

    def backup_windows_vm(self, mach_name):
        mach_uuid = self.getUUIDByName(mach_name)
        if mach_uuid is not None:
            mach_mach = argsToMach(self.ctx, [mach_name, mach_uuid])
        pass

    def restore_windows_vm(self, mach_name):
        mach_uuid = self.getUUIDByName(mach_name)
        if mach_uuid is not None:
            mach_mach = argsToMach(self.ctx, [mach_name, mach_uuid])
        pass

    def remove_windows_vm(self, mach_name):
        mach_uuid = self.getUUIDByName(mach_name)
        if mach_uuid is not None:
            mach_mach = argsToMach(self.ctx, [mach_name, mach_uuid])
            removeVm(self.ctx, mach_mach)
    
    def set_vm_resources(self, mach_name, store_path, store_mb, iso_path,
                         cpu_count: int = 2, memory_gb: int = 4):
        vbox = self.ctx['vb']
        mach_uuid = self.getUUIDByName(mach_name)
        try:
            if mach_uuid is not None:
                # get mach object & session
                mach = argsToMach(self.ctx, [mach_name, mach_uuid])
                session = self.ctx['global'].openMachineSession(mach)
                mach_session = session.machine
                # create or get storage controller object
                controller_type = self.ctx['global'].constants.StorageBus_SATA
                storage_controller = None
                controller_name = "SATA"
                for ctrl in mach_session.storageControllers:
                    if ctrl.name == controller_name and ctrl.bus == controller_type:
                        storage_controller = ctrl
                        break
                if storage_controller is None:
                    storage_controller = mach_session.addStorageController(controller_name, controller_type)
                # create hard disk object
                hdd = vbox.createMedium("vdi", store_path, 
                                    self.ctx['global'].constants.AccessMode_ReadWrite,
                                    self.ctx['global'].constants.DeviceType_HardDisk)
                hdd.createBaseStorage(store_mb * 1024 * 1024, 
                                    [self.ctx['global'].constants.MediumVariant_Standard])
                # attach hard disk object 
                for i in range(3):
                    try:
                        if hdd.state == self.ctx['global'].constants.MediumState_Created:
                            break
                        time.sleep(2)
                    except Exception as e:
                        pass
                else:
                    raise Exception("create HDD error: {}".format(hdd.state))
                mach_session.attachDevice(controller_name, 0, 0, self.ctx['global'].constants.DeviceType_HardDisk, hdd)
                # attach OS iso file
                iso = vbox.openMedium(iso_path, self.ctx['global'].constants.DeviceType_DVD, self.ctx['global'].constants.AccessMode_ReadOnly, False)
                mach_session.attachDevice(controller_name, 1, 0, self.ctx['global'].constants.DeviceType_DVD, iso)
                # attach auto install iso
                settingsFilePath = Path(mach_session.settingsFilePath)
                vmPath = settingsFilePath.parent
                autounattend = vbox.openMedium( vmPath / "autounattend.iso", self.ctx['global'].constants.DeviceType_DVD, self.ctx['global'].constants.AccessMode_ReadOnly, False)
                mach_session.attachDevice(controller_name, 2, 0, self.ctx['global'].constants.DeviceType_DVD, autounattend)
                # set CPU & memory
                mach_session.memorySize = memory_gb * 1024
                mach_session.CPUCount = cpu_count
                # save setting
                mach_session.saveSettings()
        except Exception as e:            
            pass
        finally:
            if session:
                session.unlockMachine();
        
    def getUUIDByName(self, mach_name):
        for mach in getMachines(self.ctx, True):
            try:
                if mach.name == mach_name:
                    return mach.id
            except Exception as e:
                return None
        return None

    def getSettingsFilePathByName(self, mach_name):
        for mach in getMachines(self.ctx, True):
            try:
                if mach.name == mach_name:
                    return mach.settingsFilePath
            except Exception as e:
                return None
        return None
