from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

devices = [
    {
        'device_type': 'cisco_ios',
        'ip': '172.31.177.3',
        'username': 'admin',
        'password': 'cisco',
        'template_name': 's1_config.j2'
    },
    {
        'device_type': 'cisco_ios',
        'ip': '172.31.177.4',
        'username': 'admin',
        'password': 'cisco',
        'template_name': 'r1_config.j2'
    },
    {
        'device_type': 'cisco_ios',
        'ip': '172.31.177.5',
        'username': 'admin',
        'password': 'cisco',
        'template_name': 'r2_config.j2'
    }
]

for dev in devices:
    print(f"กำลังคอนฟิกอุปกรณ์ {dev['ip']}...")
    
    template = env.get_template(dev['template_name'])
    rendered_config = template.render() 
    
    config_commands = rendered_config.splitlines()

    netmiko_params = dev.copy()
    del netmiko_params['template_name']

    with ConnectHandler(**netmiko_params) as ssh:
        output = ssh.send_config_set(config_commands)
        print(output)
        ssh.save_config()