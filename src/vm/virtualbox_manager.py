from vboxapi import VirtualBoxManager
from vboxshell import createVm
from vboxshell import startVm
from vboxshell import removeVm
from vboxshell import argsToMach

class VirtualBox:
    def __init__(self, ctx=None):
        vbox_mgr = VirtualBoxManager() 
        ctx = {
            'global': vbox_mgr,
            'vb': vbox_mgr.getVirtualBox(),
            'const': vbox_mgr.constants
        }
        self.ctx = ctx

    def create_windows_vm(self, name, arch, kind):
        createVm(self.ctx, name, arch, kind)

    def start_windows_vm(self, name):
        mach = argsToMach(self.ctx, name)
        startVm(self.ctx, mach, "gui")

    def remove_windows_vm(self, name):
        mach = argsToMach(self.ctx, name)
        removeVm(self.ctx, mach)
