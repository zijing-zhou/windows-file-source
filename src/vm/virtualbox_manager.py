from vboxapi import VirtualBoxManager
from vboxshell import createVm

class VirtualBox:
    def __init__(self, ctx=None):
        vbox_mgr = VirtualBoxManager()  # 本地管理, 可选用 "Microsoft Windows", "python"
        ctx = {
            'global': vbox_mgr,
            'vb': vbox_mgr.getVirtualBox(),
            'const': vbox_mgr.constants
        }
        self.ctx = ctx

    def create_windows_vm(self, name, arch, kind):
        createVm(self.ctx, name, arch, kind)
