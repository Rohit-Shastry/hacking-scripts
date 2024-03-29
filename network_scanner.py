import scapy.all as scapy

import optparse



def get_args():

    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="target_ip", help="Target IP/ Target IP Range")

    (options,arguments) = parser.parse_args()

    if not options.target_ip:

        print("[-] Please enter the ip range. Use --help for more info")

    return options.target_ip



def scan(ip):

    arp_request = scapy.ARP(pdst=ip)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast/arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]





    clients_list = []

    for element in answered_list:

        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}

        clients_list.append(clients_dict)

    return clients_list



def print_result(results_list):

    print("IP \t\t\t MAC Address\n-------------------------------------------")

    for client in results_list:

        print(client["ip"] + "\t\t" + client["mac"])



options = get_args()

scan_result = scan(options)

print_result(scan_result)
