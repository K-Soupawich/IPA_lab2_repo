import pytest
from netmiko import ConnectHandler

# ข้อมูลอุปกรณ์ชุดเดียวกับในไฟล์หลัก
devices = [
    {
        "device_type": "cisco_ios",
        "host": "172.31.177.3",
        "username": "admin",
        "use_keys": True,
        "key_file": "key_openssh"
    },
    {
        "device_type": "cisco_ios",
        "host": "172.31.177.4",
        "username": "admin",
        "use_keys": True,
        "key_file": "key_openssh"
    },
    {
        "device_type": "cisco_ios",
        "host": "172.31.177.5",
        "username": "admin",
        "use_keys": True,
        "key_file": "key_openssh"
    }
]

@pytest.mark.parametrize("device", devices)
def test_interface_descriptions(device):
    try:
        net_connect = ConnectHandler(**device)
        hostname = net_connect.find_prompt().strip('#')
        
        interfaces = net_connect.send_command("show interfaces description", use_textfsm=True)
        net_connect.disconnect()

        unused_port = ("0/0", "Loopback", "Vlan", "NVI")

        for intf in interfaces:
            port = intf.get('port') or intf.get('interface')
            desc = intf.get('desc') or intf.get('description')
            status = intf.get('status')

            if not port:
                continue

            if any(x in port for x in unused_port):
                continue

            if status == 'up':
                if hostname == "R2" and "0/3" in port:
                    assert desc == "Connect to WAN", f"[{hostname}] {port} expected 'Connect to WAN', but got '{desc}'"
                else:
                    assert desc.startswith("Connect to "), f"[{hostname}] {port} has invalid description: '{desc}'"
                    if desc != "Connect to PC":
                        assert " of " in desc, f"[{hostname}] {port} format does not match CDP requirement: '{desc}'"
                        
    except Exception as e:
        pytest.fail(f"Connection or test failed for {device['host']}: {e}")