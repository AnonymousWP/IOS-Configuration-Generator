"""Imports the `os` module. Sets variable for `os.getcwd()`"""

import os
dir_path = os.getcwd()

print("\n*Basic configuration*\n")
hostname = input("Enter the desired hostname: ")
secret = input("Enter the desired secret password: ") # It is strongly advised that you use a strong password.
console = input("Enter the desired console password: ") # It is strongly advised that you use a strong password.
vty = input("Enter the desired vty password: ") # It is strongly advised that you use a strong password.
interfaceList = [] # Empty list which is used later to store the interfaces in.

while True: # For a repeated input.

    choice = input("Do you want to configure a router or switch? ").lower()

    if choice == 'router':
        r = open(f"{hostname}.txt", "w") # Creates a textfile with the name of the host.
        while True:
            wantInterface = input("Do you want to configure (another) interface? ").lower()
            if wantInterface == "yes":
                interface = input("Enter the desired interface: ").lower()
                ip = input("Enter the desired IP-address: ").lower()
                sub = input("Enter the desired subnetmask: ").lower()
                description = input("Enter the desired description to the interface: ").lower()
                interfaceDict = {"interface":interface, "IP":ip, "Subnetmask":sub, "Description":description} # Creates a dictionary with characteristics of an interface.
                interfaceList.append(interfaceDict)
            elif wantInterface == "no":
                break

        username = input("Enter the desired username for SSH access: ")
        password = input("Enter the desired password for SSH access: ") # It is strongly advised that you use a strong password.
        domainName = input("Enter the desired domain name. This is necessary to setup SSH keys: ").lower()

        while True:
            encryption = input("Do you want to apply encryption? Yes or no? ").lower()
            if encryption == 'yes':
                encryption1 = "service password-encryption"
                break
            elif encryption == 'no':
                encryption1 = "no service password-encryption"
                break
            else:
                print("Incorrect input")
                continue
        interfaceConfiguration = "" # Empty string to store the interfaceconfiguration below in.
        for value in interfaceList:
            interfaceConfiguration = interfaceConfiguration + "interface " + value["interface"] + "\n" + "ip address " + value["IP"] + " " + value["Subnetmask"] + "\n" + "description " + value["Description"] + "\n" + "no shutdown\n" # To later get the values from the dictionary.
        banner = input("Enter the desired banner: ")

        # Writes the commands (including user input) to the file.
        r.write(f"enable\nconfigure terminal\n!\nhostname {hostname}\n!\n"
                "no ip domain lookup\n"
                f"enable secret {secret}\n!\n"
                f"banner motd # {banner}#\n!\n"
                f"username {username} privilege 15 password 0 {password}\n!\n{interfaceConfiguration}!\n"
                f"ip domain name {domainName}\n"
                "line console 0\n"
                "exec-timeout 0 0\n"
                "privilege level 15\n"
                f"password {console}\n"
                "login\n"
                "logging synchronous\n!\n"
                "line vty 0 15\n"
                f"password {vty}\n"
                "login local\n"
                "transport input ssh\n!\n"
                "exit\n"
                "crypto key generate rsa general-keys modulus 2048\n"
                f"ip ssh version 2\n!\n{encryption1}\n!\n")

        while True: # For a repeated input.
            routing = input("Do you want to use a routing protocol? The available option is OSPF: ").lower()
            if routing == "yes":
                routingList = [] # Empty list which is used later to store the routing entries in.
                while True:
                    routingID = input("Enter the desired routerID for OSPF. Type 'end' to stop: ")
                    if routingID == "end":
                        break
                    routingInstance = {"routerID": routingID, "areas": []} # Dictionary of routing ID and areas.
                    while True:
                        areaNumber = input("Enter the desired area number for OSPF. Type 'end' to stop: ")
                        if areaNumber == "end":
                            break
                        routingInput = input("Enter the desired network addresses: ").lower()
                        routingArea = {"routerArea": areaNumber, "networkAddress": routingInput} # Dictionary of area numbers and network addresses.
                        routingInstance ["areas"].append(routingArea) # Stores the areas in the dictionary.
                    routingList.append(routingInstance) # Stores the routing values (dictionary) in a list.
                routingConfiguration = ""
                # Does a for-loop in the routinglist, where the dictionary is in, to obtain the values.
                for value in routingList:
                    routingConfiguration = routingConfiguration + "router ospf  " + value["routerID"] + "\n"
                    for area in value["areas"]:
                        routingConfiguration = routingConfiguration + "area " + area["routerArea"] + "\n"
                        routingConfiguration = routingConfiguration + "network " + area["networkAddress"] + "\n"
                r.write(routingConfiguration)
                break # Explicitly breaks out of the While-loop so that it continues with the rest of the script.
            elif routing == "no":
                break
            else:
                print("Wrong value")
        while True:
            static = input("Do you want to add (another) static route? Yes or no? ").lower()
            if static == "yes":
                staticIP = input("Enter the desired IP-address for the static route: ").lower()
                staticSub = input("Enter the desired subnetmask for the static route: ").lower()
                nextHop = input("Enter the next-hop address or the interface for the static route: ").lower()
                r.write(f"!\nip route {staticIP} {staticSub} {nextHop}\n")
            elif static == "no":
                break

        while True:
            r.write("!\n")
            saveConfig = input("Do you want to copy your running configuration to the startup configuration? ")
            if saveConfig == "yes":
                r.write("do write")
                break
            elif saveConfig == "no":
                print("Running configuration won't be saved; if you reboot your intermediary network device, you'll lose the configuration you've set.")
                break
            else:
                print("You didn't choose a(n) (correct) option. Please try again.")
        r.close()
        break # Explicit break so that the input "Do you want to configure a router or switch? " is not being returned again.

    elif choice == 'switch':
        s = open(f"{hostname}.txt", "w") # Creates a textfile with the name of the host.
        domainName = input("Enter the desired domain name. This is necessary to setup SSH keys: ").lower()

        # Writes the commands (including user input) to the file.
        s.write(f"enable\nconfigure terminal\n!\nhostname {hostname}\n!\n"
                f"enable secret {secret}\n!\n"
                "line console 0\n"
                "exec-timeout 0 0\n"
                "privilege level 15\n"
                f"password {console}\n"
                "login\n"
                "logging synchronous\n!\n"
                "line vty 0 15\n"
                f"password {vty}\n"
                "login local\n"
                "transport input ssh\n!\n"
                f"ip domain-name {domainName}\n")

        vlan = [] # VLAN ID will be stored in this empty list.
        name = [] # VLAN name will be stored in this empty list.
        while True:

            try:
                vlanInput = int(input("Enter a VLAN-id. Type '0' to stop: ").lower())
            except ValueError:
                print("Enter a number")
                continue

            if vlanInput < 0:
                continue
            elif vlanInput == int(0):
                break
            else:
                nameInput = input("Enter the desired name of the vlan: ").lower()
                vlan.append(vlanInput) # Stores the vlanInput in the empty list.
                name.append(nameInput) # Stores the nameInput in the empty list.

        """Aggregates `vlan` and `name` in a tuple and writes the values in the text file."""
        zipped = zip(vlan, name)
        lists = list(zipped)
        for i in lists:
            s.write("vlan " + str(i[0]) + "\n")
            s.write("name " + i[1] + "\n!\n")

        while True:
            layer = input("What kind of switch do you want to configure? Layer 2 or 3? Enter a number: ").lower()

            s.write("crypto key generate rsa general-keys modulus 2048\nip ssh version 2\n!\n")

            if layer == '2':
                while True:
                    reach = input("Do you want to enter (another) range? Yes or no? Type 'end' to stop: ").lower()
                    if reach == "yes":
                        interfaces = input("Enter the desired range of interfaces: ").lower()
                        s.write(f"interface range {interfaces}\nduplex full \n")
                    elif reach == "no":
                        interface = input("Enter an interface to configure: ").lower()
                        s.write(f"interface {interface}\nduplex full \n")
                    elif reach == "end":
                        break
                    else:
                        print("You didn't choose an available option. Try again.")
                        continue

                    switchport = input("Do you want to set the switchport in trunk or access mode? ").lower()
                    if switchport == "access":
                        s.write("switchport mode access \n")
                        access = input("Enter the VLAN-id that's allowed on these interfaces: ")
                        s.write(f"switchport access vlan {access}\n!\n")
                    elif switchport == "trunk":
                        s.write("switchport mode trunk \n!\n")
                    else:
                        print("Wrong value. Try again.")
                        s.write("!\n")
                        continue
                break # Explicit break so that the input "What kind of switch do you want to configure?" is not being returned again.

            elif layer == '3':
                s.write("ip routing \n!\n")
                while True:
                    try:
                        vlanID = int(input("Enter a VLAN-id. Type '0' to stop: ").lower())
                    except ValueError:
                        print("Enter a number")
                        continue

                    if vlanID < 0:
                        continue
                    elif vlanID == int(0):
                        break
                    else:
                        s.write("interface vlan " + str(vlanID) + "\n")
                        description = input("Enter the desired description of the VLAN: ").lower()
                        s.write(f"description {description}\n")
                        ipAddress = input("Enter the desired IP-address: ")
                        sub = input("Enter the desired subnetmask: ").lower()
                        s.write(f"ip address {ipAddress} {sub}\n!\n")

                while True:
                    static = input("Do you want to add (another) static route? Yes or no? ")

                    if static == "yes":
                        staticIP = input("Enter an IP-address for the static route: ").lower()
                        staticSub = input("Enter a subnetmask for the static route: ").lower()
                        nextHop = input("Enter a next-hop address or interface for the static route: ").lower()
                        s.write(f"ip route {staticIP} {staticSub} {nextHop} \n")
                    elif static == "no":
                        break
                    else:
                        print("You didn't choose any of the available options. Try again.")
                        continue
                break # Explicit break so that the input "What kind of switch do you want to configure?" is not being returned again.
            else:
                print("You didn't choose any of the available options. Try again.")
                continue
        while True:
            saveConfig = input("Do you want to copy your running configuration to the startup configuration?\n")
            if saveConfig == "yes":
                s.write("do write")
                break
            elif saveConfig == "no":
                print("\n*WARNING:* Running configuration won't be saved; if you reboot your intermediary network device, you'll lose the configuration you've set.\n")
                break
            else:
                print("You didn't choose a(n) (correct) option. Please try again.\n")
        s.close()
        break # Explicit break so that the input "What kind of switch do you want to configure?" is not being returned again.

    else:
        print("You didn't choose any of the available options. Try again.\n")
        continue
print(f"\nConfig file for {hostname} has been made. You can find it back in: {dir_path}")
