#!/usr/bin/env python
import subprocess as sp
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    options, arguments = parser.parse_args()
    if not options.interface:
        parser.error("[-] input valid interface, use --help for info.")
    elif not options.new_mac:
        parser.error("[-] input valid new mac, use --help for info.")
    return options


def change_mac(interface, new_mac):
    print("[+] change mac address for {} to {}".format(interface, new_mac))
    sp.call(["ifconfig", interface, "down"])
    sp.call(["ifconfig", interface, "hw", "ether", new_mac])
    sp.call(["ifconfig", interface, "up"])

def get_curr_mac(interface):
    ifconfig_result = str(sp.check_output(["ifconfig", interface]))
    mac_add_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_add_search_result:
        return mac_add_search_result.group(0)
    else:
        print("[-] Could not read mac address.")


options = get_arguments()
oldCurr_mac = get_curr_mac(options.interface)
print("Current mac = " + str(oldCurr_mac))

change_mac(options.interface, options.new_mac)
newCurr_mac = get_curr_mac(options.interface)
print("Current mac = " + str(newCurr_mac))
if newCurr_mac == options.new_mac:
    print("[+] MAC successfully changed.")
else:
    print("[-] MAC change unsuccessful.")


