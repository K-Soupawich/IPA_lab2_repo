import paramiko
import time

devices = [
    {"name": "R0", "ip": "172.31.177.1"},
    {"name": "S0", "ip": "172.31.177.2"},
    {"name": "S1", "ip": "172.31.177.3"},
    {"name": "R1", "ip": "172.31.177.4"},
    {"name": "R2", "ip": "172.31.177.5"}
]

username = "admin"
private_key_path = "window_user"

def main():
    # print("Starting Paramiko SSH Key-based Authentication...\n")
    # print("-" * 50)

    try:
        my_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        # print("private key loaded")
    except Exception as e:
        print(f"Error loading private key: {e}")
        return

    for dev in devices:
        print(f"Connecting to {dev['name']} ({dev['ip']})")
        client = paramiko.SSHClient()
        
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            client.connect(
                hostname=dev['ip'],
                port=22,
                username=username,
                pkey=my_key,
                look_for_keys=False,
                allow_agent=False,
                timeout=10
            )
            # print(f"  [+] SSH Login to {dev['name']} SUCCESSFUL!")
            
            stdin, stdout, stderr = client.exec_command("show ip interface brief | exclude unassigned")
            time.sleep(1)
            output = stdout.read().decode('ascii')
            # print(f"  [>] Output from {dev['name']}:")
            print(output.strip())
            
        except paramiko.AuthenticationException:
            print(f"Authentication Failed on {dev['name']}")
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(f"Connection Refused on {dev['name']}")
        except Exception as e:
            print(f"Error on {dev['name']}: {e}")
        finally:
            client.close()
            print("-" * 50)

if __name__ == "__main__":
    main()