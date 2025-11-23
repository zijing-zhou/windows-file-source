import xml.etree.ElementTree as ET
import os

def get_vbox_vm_config(vbox_file_path):
    if not os.path.exists(vbox_file_path):
        print(f"Error: File '{vbox_file_path}' does not exist. Please check the path.")
        return None

    try:
        tree = ET.parse(vbox_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing .vbox file: {e}")
        return None
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return None

    config = {}

    machine_element = root.find('Machine')
    if machine_element is None:
        print("Warning: 'Machine' element not found.")
        return None

    config['Name'] = machine_element.get('name')
    config['UUID'] = machine_element.get('uuid')
    config['OSType'] = machine_element.get('OSType')

    hardware_element = machine_element.find('Hardware')
    if hardware_element:
        config['CPUCount'] = hardware_element.get('CPUCount')
        config['MemorySizeMB'] = hardware_element.get('MemorySize')
        config['VRAMSizeMB'] = hardware_element.get('VRAMSize')

        network_adapters = []
        for adapter in hardware_element.findall('NetworkAdapters/Adapter'):
            adapter_info = {
                'slot': adapter.get('slot'),
                'enabled': adapter.get('enabled'),
                'type': adapter.get('type'),
                'attachment': adapter.get('attachment'),
                'MACAddress': adapter.get('MACAddress')
            }
            network_adapters.append(adapter_info)
        config['NetworkAdapters'] = network_adapters

        storage_controllers = []
        for controller in hardware_element.findall('StorageControllers/StorageController'):
            controller_info = {
                'name': controller.get('name'),
                'type': controller.get('ControllerType'),
                'portcount': controller.get('PortCount'),
                'devices': []
            }
            for device in controller.findall('AttachedDevice'):
                device_info = {
                    'type': device.get('type'),
                    'port': device.get('port'),
                    'device': device.get('device'),
                    'image_path': None
                }
                image = device.find('Image')
                if image is not None:
                    image_path = image.get('uuid')
                    if image.get('type') == 'HardDisk':
                        hard_disks_element = root.find('Global/HardDisks')
                        if hard_disks_element:
                            for hard_disk in hard_disks_element.findall('HardDisk'):
                                if hard_disk.get('uuid') == image_path:
                                    device_info['image_path'] = hard_disk.get('location')
                                    break
                    elif image.get('type') == 'DVD':
                        device_info['image_path'] = image.get('location')
                    elif image.get('type') == 'Floppy':
                        device_info['image_path'] = image.get('location')

                controller_info['devices'].append(device_info)
            storage_controllers.append(controller_info)
        config['StorageControllers'] = storage_controllers

    return config

if __name__ == "__main__":
    vbox_file_path_to_use = "MyVM.vbox"

    vm_config = get_vbox_vm_config(vbox_file_path_to_use)

    if vm_config:
        print("\n--- VM Configuration Details ---")
        for key, value in vm_config.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")
        print("--------------------------------")
    else:
        print("Failed to retrieve VM configuration.")
