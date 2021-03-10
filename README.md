# IOS-Configuration-Generator

 A (Python- and PowerShell-based) script that generates commands/configurations for Cisco routers and switches that run IOS. It's meant for IOS users who are too lazy (and/or don't have experience with Network Automation-related solutions, such as Ansible) to configure everything themselves. By using this script, you can create a template for yourself. All you have to do after you ran the script, is simply copy-paste the output (which is in the .txt file) in IOS.

## Notes
 
 - It may be possible that some commands don't work, as over time with different versions of IOS, commands change. Feel free to make an issue, or create a PR to contribute. I have tested the generated router and switch configurations on a Cisco 1941 router and Cisco 2960-24TT switch in Cisco Packet Tracer 7.3.1, so that again means that commands on a physical router or switch may differ. Packet Tracer is usually more limited in the amount of supported commands.
 - The PowerShell script is more limited and harder for me to maintain, so it won't be updated as much as the Python script.
 - All commands that are outputted are not in the short form, so that for new IOS-users, it's more understandable of what they are doing and configuring.
 - Make sure you are putting the right interfaces. Don't know which interfaces there are attached? Execute `show ip interface brief` in the Privileged EXEC Mode to see which interfaces are present.
 - The generated configurations are not 100% tested (yet). If there are any issues: file an issue in this repository.
 - Mind that I'm not a developer, but I do this as a hobby. When I made this script, it was not focused on making the script looking as clean/efficient as possible. If you feel like improving it, feel free to create a Pull Request.
 - This project is still WIP (Work-In-Progress), so do remember that it may lack some functions. Feel free to create a Pull Request or issue.

## To be added:

 - [x] Add possibility to configure multiple OSPF IDs, areas and network addresses

This repository offers two scripts:

1. A Python-script that offers most basic functionality. It offers the following features:

- Enable
- Configure terminal
- Hostname
- No domain lookup (preventing domain lookups, resulting in having to wait for X amount of seconds before you can continue configuring)
- Configuring console lines
- Configuring VTY lines (for remote control)
- Password for IOS
- Password for console line
- Password for the vty line
- Whether you want to configure a switch (both layer 2 and layer 3 are supported) or router
- (Ranges of) interfaces (automatically does a `no shutdown` after setting an IP-address as well)
- IP-addresses
- Subnetmasks
- Description for interfaces
- Username for SSH access
- Password for SSH access
- Domain names
- SSH and generating 2048-bit RSA keys
- Password encryption
- Banner MOTD (Message Of The Day)
- Routing (OSPF)
- Static routes
- VLAN IDs
- Putting VLANs in either trunk or access mode
- IP-routing
- Copying the running config to the startup config (with a `do write`)

## Sample output

#### Example configuration for a **router**, generated with the Python script:

```
enable
configure terminal
!
hostname R1
!
no ip domain lookup
enable secret class
!
banner motd # Unauthorized access is prohibited.#
!
username admin privilege 15 password 0 sshclass
!
interface gigabitethernet0/0
ip address 192.168.1.1 255.255.255.0
description to r2
no shutdown
interface gigabitethernet0/1
ip address 192.168.2.1 255.255.255.0
description to s1
no shutdown
!
ip domain name test.test
line console 0
exec-timeout 0 0
privilege level 15
password consoleclass
login
logging synchronous
!
line vty 0 15
password vtyclass
login local
transport input ssh
!
exit
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
!
service password-encryption
!
router ospf  1
network 192.168.3.0 0.0.0.255 area 0
!
ip route 192.168.4.0 255.255.255.0 192.168.3.2
!
do write
```

#### Example configuration **a layer 2 switch**, generated with the Python script:

```
enable
configure terminal
!
hostname S1
!
enable secret class
!
line console 0
exec-timeout 0 0
privilege level 15
password consoleclass
login
logging synchronous
!
line vty 0 15
password vtyclass
login local
transport input ssh
!
ip domain-name test.test
vlan 10
name test
!
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
!
interface range gigabitethernet 0/1 - 2
duplex full
switchport mode trunk
no shutdown
!
interface range fastethernet0/1 - 3
duplex full 
switchport mode access 
switchport access vlan 10
no shutdown
!
do write
```

#### Example configuration **a layer 3 switch**, generated with the Python script:

```
enable
configure terminal
!
hostname S1
!
enable secret cisco
!
line console 0
exec-timeout 0 0
privilege level 15
password class
login
logging synchronous
!
line vty 0 15
password vtyclass
login local
transport input ssh
!
ip domain-name test.com
vlan 5
name test
!
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
!
ip routing 
!
interface vlan 10
description test2
ip address 192.168.3.1 255.255.255.0
!
ip route 192.168.1.1 255.255.255.0 192.168.2.1
do write
```

2. A PowerShell-script that offers basic functionality, but is much more limited than the Python script.

