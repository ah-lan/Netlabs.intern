from netmiko import ConnectHandler
import getpass

# Device connection details
device = {
    'device_type': 'cisco_ios_telnet',
    'host': '192.168.30.30',
    'password': getpass.getpass("Enter Telnet password: "),  # Only password required
    'port': 23,
    'secret': getpass.getpass("Enter enable password: "),  # For privileged mode
}

# VLAN to port mapping configuration
vlan_assignments = {
    10: range(1, 6),    # Ports 1-5 for VLAN 10
    20: range(6, 11),   # Ports 6-10 for VLAN 20
    30: range(11, 16)    # Ports 11-15 for VLAN 30
}

try:
    # Connect to the device
    print(f"\nConnecting to {device['host']} via Telnet...")
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    print("Successfully connected and entered enable mode!")

    # Configure the VLANs and ports
    for vlan_id, ports in vlan_assignments.items():
        # Create VLAN (if it doesn't exist)
        print(f"\nCreating VLAN {vlan_id}...")
        net_connect.send_config_set([f"vlan {vlan_id}", f"name VLAN_{vlan_id}"])
        
        # Configure each port in this VLAN
        for port in ports:
            interface = f"GigabitEthernet1/0/{port}"
            print(f"Configuring {interface} for VLAN {vlan_id}...")
            config_commands = [
                f"interface {interface}",
                "switchport mode access",
                f"switchport access vlan {vlan_id}",
                f"description VLAN_{vlan_id}_Access_Port",
                "no shutdown"
            ]
            net_connect.send_config_set(config_commands)

    # Verification
    print("\nVerifying VLAN configuration...")
    print(net_connect.send_command("show vlan brief"))

    print("\nVerifying interface status...")
    print(net_connect.send_command("show ip interface brief"))

    # Save configuration
    print("\nSaving configuration to NVRAM...")
    net_connect.send_command("write memory")

    # Disconnect
    net_connect.disconnect()
    print("\nConfiguration complete! Disconnected from device.")

except Exception as e:
    print(f"\nAn error occurred: {str(e)}")