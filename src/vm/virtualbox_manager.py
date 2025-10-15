from vboxapi import VirtualBoxManager
from vm.vboxshell import createVm
from vm.vboxshell import startVm
from vm.vboxshell import removeVm
from vm.vboxshell import argsToMach
from vm.vboxshell import getMachines

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
        
    def set_vm_resources(self, name, cpu_count: int = 2, memory_gb: int = 4):
        vbox = self.ctx['vb']
        uuid = self.getUUIDByName(name)
        if uuid is not None:
            mach = argsToMach(self.ctx, [name, uuid])
            session = self.ctx['global'].openMachineSession(mach, fPermitSharing=True)
            mach = session.machine
            try:
                m = mach
                m.MemorySize = memory_gb * 1024
                m.CPUCount = cpu_count
                m.saveSettings()
            finally:
                session.unlockMachine()

    def getUUIDByName(self, name):
        for mach in getMachines(self.ctx, True):
            try:
                if mach.name == name:
                    return mach.id
            except Exception as e:
                return None
        return None

