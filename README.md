# IOS-Configuration-Generator
 A (Python- and PowerShell-based) script that generates commands/configurations for Cisco routers and switches that run IOS. It's meant for IOS users who are too lazy (and don't have experience with Network Automation-related solutions, such as Ansible) to configure everything themselves. By using this script, you can create a template for yourself. All you have to do after you ran the script, is simply copy-paste the output (which is in the .txt file) in IOS.

 **NOTES:** 
 
 - It may be possible that some commands don't work, as over time with different versions of IOS, commands change. Feel free to make an issue, or create a PR to contribute. I have tested the generated router and switch configurations on a Cisco 1941 router and Cisco 2960-24TT switch.
 - The PowerShell script is more limited and harder for me to maintain, so it'll be available in the PowerShell branch.
 - All commands that are outputted are not in the short form, so that for new IOS-users, it's more understandable of what they are doing and configuring.
 - Make sure you are putting the right interfaces. Don't know which interfaces there are attached? Execute `show ip interface brief` in the Privileged EXEC Mode to see which interfaces are present.

This repository offers two scripts:

1. A Python-script that offers most basic functionality. It offers the following features:

- Enable
- Configure terminal
- Hostname
- no ip domain-lookup
- Configuring console lines
- Configuring VTY lines (for remote control)
- Password for IOS
- Password for console line
- Password for the vty line
- Whether you want to configure a switch or router
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
- Routing (RIP version 2, as of now. OSPF may be added later)
- Static routes
- VLAN IDs
- Putting VLANs in either trunk or access mode
- IP-routing
- Copying the running config to the startup config (with a `do wr`)


2. A PowerShell-script that offers basic functionality, but is much more limited than the Python script.

## Sample output

### Configuration for a **router**, generated with the Python script:

```
enable
configure terminal
!
hostname R1
!
no ip domain-lookup
enable secret cisco
!
banner motd # no access allowed for unauthorised personnel. #
!
username admin privilege 15 password 0 SSHclass
!
interface gigabitethernet0/0
description to r2
ip address 192.168.1.1 255.255.255.0
no shutdown
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
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
!
service password-encryption
!
router rip
version 2
network 192.168.2.0
!
ip route 192.168.3.1 255.255.255.0 192.168.3.2
!
do write
```

### Configuration for **a layer 2 switch**, generated with the Python script:

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
interface range gigabitethernet0/1-2
duplex full 
switchport trunk encapsulation dot1q 
switchport mode trunk 
!
interface fastethernet0/1
duplex full 
switchport mode access 
switchport access vlan 5
!
do write
```

### Configuration for **a layer 3 switch**, generated with the Python script:

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