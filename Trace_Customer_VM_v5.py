# -*- coding: utf-8 -*-
"""
Created on Thu May  3 12:06:43 2018

@author: nigam
"""

""" Checking ARP Entry"""

device_ip = "146.89.4.3"



import getpass
import paramiko

print ("============================================")

userIPaddress = raw_input("Enter Customer VM IP Adress for Tracing: ")

print ("============================================")
site_id = raw_input("Enter Site 3 digit code: ")

print ("============================================")
custom_username = raw_input("Enter Username : ")
print ("============================================")

print ("\n")
print ("============================================")
custom_password = getpass.getpass("Enter Password : ")
print ("============================================")

def call_second_switch(arp_string, device_ip, custom_username, custom_password):
    # This is second switch function it can be other core or ToR
    vm_find_apr = paramiko.SSHClient()
    vm_find_apr.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    vm_find_apr.connect(device_ip, port=22, username=custom_username, password=custom_password)
    command_string1 = "show ethernet-switching table | match "
    command_string2 = " | trim 55"
    main_command = command_string1 + arp_string + command_string2
    stdin1, stdout1, stderr1 = vm_find_apr.exec_command(main_command)
    ether_string = stdout1.readline()
    count_chr = len(ether_string)
    count_chr = count_chr - 2
    ether_interface = ether_string[0:count_chr]
    print (ether_interface)
    if ether_interface != "":                
        command_string1 = "show lldp neighbors | match "
        main_command = command_string1 + ether_interface
        stdin1, stdout1, stderr1 = vm_find_apr.exec_command(main_command)
        lldp_neighbour_info = stdout1.readline()
        lldp_interface = ""
        for i in range(0, len(lldp_neighbour_info)):
            first_chr = lldp_neighbour_info[i]
            if first_chr != ".":
                lldp_interface = lldp_interface + first_chr
            else:
                break
    command_string1 = "show lldp neighbors interface "
    command_string2 = " | match System | except Description | except capabilities | trim 21"
    main_command = command_string1 + lldp_interface + command_string2
    stdin1, stdout1, stderr1 = vm_find_apr.exec_command(main_command)
    neighbour_system_name = stdout1.readline()
    
    if "rsf" in neighbour_system_name or "csw" in neighbour_system_name or "rsc" in neighbour_system_name:
        vm_find_apr.close() # Second switch connection is getting closed here
        #call_third_switch(arp_string, device_ip, custom_username, custom_password) # Call function to login into third switch
        print "We need to Call third Switch"
    else:
        vm_find_apr.close() # Second switch connection is getting closed here
        print "This is Last Switch"
        
    
    

def check_arp(device_ip,custom_username,custom_password,userIPaddress):
    command_string1 = "show arp | match "
    vm_find_apr = paramiko.SSHClient()
    vm_find_apr.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    main_command = command_string1 + userIPaddress

    vm_find_apr.connect(device_ip, port=22, username=custom_username, password=custom_password)
    stdin, stdout, stderr = vm_find_apr.exec_command(main_command)

    arp_string = stdout.readline()
    ether_interface = ""

    if arp_string != "":
        arp_string = arp_string[0:17]
        command_string1 = "show ethernet-switching table | match "
        command_string2 = " | trim 55"
        main_command = command_string1 + arp_string + command_string2
        stdin1, stdout1, stderr1 = vm_find_apr.exec_command(main_command)
        ether_string = stdout1.readline()
        count_chr = len(ether_string)
        count_chr = count_chr - 2
        ether_interface = ether_string[0:count_chr]
        print (ether_interface)
        
        if ether_interface != "":                
            command_string1 = "show lldp neighbors | match "
            main_command = command_string1 + ether_interface
            stdin1, stdout1, stderr1 = vm_find_apr.exec_command(main_command)
            lldp_neighbour_info = stdout1.readline()
            lldp_interface = ""
            for i in range(0, len(lldp_neighbour_info)):
                first_chr = lldp_neighbour_info[i]
                if first_chr != ".":
                    lldp_interface = lldp_interface + first_chr
                else:
                    break

            command_string1 = "show lldp neighbors interface "
            command_string2 = " | match address | except Chassis | except Neighbour  | trim 28"
            main_command = command_string1 + lldp_interface + command_string2
            stdin1, stdout1, stderr1 = vm_find_apr.exec_command(main_command)
            neighbour_switch_ip = stdout1.readline()
            #neighbour_switch_ip = stdout1.readline()
            if neighbour_switch_ip != "":
                device_ip = (neighbour_switch_ip)
                command_string1 = "show lldp neighbors interface "
                command_string2 = " | match System | except Description | except capabilities | trim 21"
                main_command = command_string1 + lldp_interface + command_string2
                stdin1, stdout1, stderr1 = vm_find_apr.exec_command(main_command)
                neighbour_system_name = stdout1.readline()
                vm_find_apr.close() # First switch connection is getting closed here
                if "rsf" in neighbour_system_name or "csw" in neighbour_system_name or "rsc" in neighbour_system_name:
                    
                # Call function to login inot second switch
                    call_second_switch(arp_string, device_ip, custom_username, custom_password)
                else:
                    print "This is Last Switch"
            else:
                print "No LLDP information Found"
        else:
            print "No Ethernet Switch table value found"
    else:
        print "No ARP find"
        vm_find_apr.close()

    

if site_id == "RTPS":
    check_arp(device_ip,custom_username,custom_password,userIPaddress)

