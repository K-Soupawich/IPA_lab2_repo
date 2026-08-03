from netmiko import ConnectHandler

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

for device in devices:
    try:
        net_connect = ConnectHandler(**device)
        hostname = net_connect.find_prompt().strip('#')
        print(f"\nConfig {hostname}")

        cdp_neighbors = net_connect.send_command("show cdp neighbors", use_textfsm=True)
        interfaces = net_connect.send_command("show ip interface brief", use_textfsm=True)

        config_commands = []
        cdp_ports = []

        if isinstance(cdp_neighbors, list):
            for neighbor in cdp_neighbors:
                local_port = neighbor.get('local_interface').replace("Gig ", "G")
                remote_port = neighbor.get('platform').replace("Gig", "G") + neighbor.get('neighbor_interface')

                # print("port", neighbor.get('platform'))
                
                remote_dev = neighbor.get('neighbor_name').split('.')[0]
                
                if local_port and remote_port:
                    if "0/0" in local_port or "Loopback" in local_port:
                        continue
                        
                    desc = f"Connect to {remote_port} of {remote_dev}"
                    config_commands.extend([f"interface {local_port}", f"description {desc}"])
                    cdp_ports.append(local_port)

        if isinstance(interfaces, list):
            for intf in interfaces:
                port = intf.get('interface')
                if not port:
                    continue

                unused_port = ("0/0", "Loopback", "Vlan", "NVI")

                if any(x in port for x in unused_port):
                    continue
                    
                short_port = port.replace("GigabitEthernet", "G")
                
                if hostname == "R2" and (port == "GigabitEthernet0/3"):
                    config_commands.extend([f"interface {short_port}", "description Connect to WAN"])
                
                elif intf.get('status') == 'up' and short_port not in str(cdp_ports):
                    if not (hostname == "R2" and "0/3" in port):
                        config_commands.extend([f"interface {short_port}", "description Connect to PC"])

        if config_commands:
            print(f"Sending configurations: {config_commands}")
            net_connect.send_config_set(config_commands)
            net_connect.save_config()
        net_connect.disconnect()

    except Exception as e:
        print(f"Failed to process {device['host']}: {e}")