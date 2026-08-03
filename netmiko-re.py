import re
from netmiko import ConnectHandler

# กำหนดข้อมูลของ Router ทั้งสองตัว
router1 = {
    "device_type": "cisco_ios",
    "host": "172.31.177.4",
    "username": "admin",
    "use_keys": True,
    "key_file": "key_openssh"
}

router2 = {
    "device_type": "cisco_ios",
    "host": "172.31.177.5",
    "username": "admin",
    "use_keys": True,
    "key_file": "key_openssh"
}

routers = [router1, router2]

uptime_pattern = re.compile(r"uptime is (.*)")

intf_pattern = re.compile(r"^(\S+)\s+(?:\S+)\s+\w+\s+\w+\s+(up)\s+(up)", re.MULTILINE)

for device in routers:
    print(f"\n[{device['host']}] Connecting...")
    try:
        net_connect = ConnectHandler(**device)
        
        sh_ver = net_connect.send_command("show version")
        uptime_match = uptime_pattern.search(sh_ver)
        uptime = uptime_match.group(1)
        
        sh_ip_int = net_connect.send_command("show ip interface brief")
        active_interfaces = []
  
        for match in intf_pattern.finditer(sh_ip_int):
            interface_name = match.group(1)
            active_interfaces.append(interface_name)
            
        print(f"Router: {device['host']}")
        print(f"Uptime: {uptime}")
        print(f"Active Interfaces:")
        for int in active_interfaces:
            print(f" -{int}")
        
        net_connect.disconnect()
        
    except Exception as e:
        print(f"[{device['host']}] Connection failed: {e}")