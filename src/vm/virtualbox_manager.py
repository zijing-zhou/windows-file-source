
import os
import subprocess
import time
import shutil
import json
from vboxapi import VirtualBoxManager

class VirtualBoxManager:
    def create_windows_vm(self, vm_name, os_type_id, vm_memory_size):
        vbox_mgr = VirtualBoxManager(None, None)
        vbox = vbox_mgr.mgr.getVirtualBox()
        session = vbox_mgr.mgr.getSessionObject(vbox)
        sFlags = ''
        sCipher = '' ## @todo No encryption support here yet!
        sPasswordID = ''
        sPassword = ''
        # TODO: amd64: 1
        machine = vbox.createMachine("", vm_name, , [], os_type_id, sFlags, sCipher, sPasswordID, sPassword)
        machine.saveSettings()
        vbox.registerMachine(machine)
        machine.lockMachine(session, vbox_mgr.constants.LockType_Write)
        try:
            session.machine.memorySize = vm_memory_size
            session.machine.saveSettings()
        finally:
            session.unlockMachine()
        vbox_mgr = None
