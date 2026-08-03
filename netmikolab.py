from netmiko import ConnectHandler

common_settings = {
    "device_type": "cisco_ios",
    "username": "admin",
    "use_keys": True,
    "key_file": "key_openssh", 
}

devices = [
    {"name": "S1", "host": "172.31.177.3"},
    {"name": "R1", "host": "172.31.177.4"},
    {"name": "R2", "host": "172.31.177.5"}
]

config_s1 = [
    "vlan 101",
    "name control-data",
    "exit",
    "int g0/1",
    "switchport mode access",
    "switchport access vlan 101"

    "ip access-list standard MGT_ACCESS",
    "permit 172.31.177.0 0.0.0.15",
    "permit 10.30.6.0 0.0.0.255",
    "exit",
    "line vty 0 4",
    "access-class MGT_ACCESS in",
    "exit"
]

config_r1 = [
    "router ospf 1 vrf control-data",
    "exit",
    "interface g0/1",
    "ip ospf 1 area 0",
    "interface g0/2",
    "ip ospf 1 area 0",
    "interface loopback0",
    "ip ospf 1 area 0",
    "exit",

    "ip access-list standard MGT_ACCESS",
    "permit 172.31.177.0 0.0.0.15",
    "permit 10.30.6.0 0.0.0.255",
    "exit",
    "line vty 0 4",
    "access-class MGT_ACCESS in",
    "exit"
]

config_r2 = [
    "router ospf 1 vrf control-data",
    "default-information originate",
    "exit",
    "interface g0/1",
    "ip ospf 1 area 0",
    "ip nat inside",
    "interface g0/2",
    "ip ospf 1 area 0",
    "ip nat inside",
    "interface loopback0",
    "ip ospf 1 area 0",
    "exit",
    
    "interface g0/3",
    "ip nat outside",
    "exit",
    
    "ip access-list standard LAB2_NAT",
    "permit any",
    "exit",
    "ip nat inside source list LAB2_NAT interface g0/3 vrf control-data overload",

    "ip access-list standard MGT_ACCESS",
    "permit 172.31.177.0 0.0.0.15",
    "permit 10.30.6.0 0.0.0.255",
    "exit",
    "line vty 0 4",
    "access-class MGT_ACCESS in",
    "exit"
]

for dev in devices:
    connection_params = {**common_settings, "host": dev["host"]}
    try:
        with ConnectHandler(**connection_params) as net_connect:
            print(f"กำลังตั้งค่า {dev['name']}...")
            
            if dev['name'] == 'S1':
                net_connect.send_config_set(config_s1)
            elif dev['name'] == 'R1':
                net_connect.send_config_set(config_r1)
            elif dev['name'] == 'R2':
                net_connect.send_config_set(config_r2)
                
            net_connect.save_config()
            print(f"ตั้งค่า {dev['name']} สำเร็จ!")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดกับ {dev['name']}: {e}")