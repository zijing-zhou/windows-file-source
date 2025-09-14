
import vboxshell


class VirtualBoxManager:
    ctx = None

    def __init__(ctx):
        self.ctx = ctx
    
    def create_windows_vm(self, name, arch, kind, memerysize):
        vboxshell.createVm(self.ctx, name, arch, kind, memerysize)
        
    def start_vm(self, ctx, mach, vmtype):
        vboxshell.startVm(self.ctx, mach, vmtype)


